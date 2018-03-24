#!/usr/bin/env python

# Copyright 2016 The Kubernetes Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import logging
import os
import subprocess
import time
import traceback
import yaml
from pprint import pprint

from subprocess import PIPE

from data import Parser, ResultDb
from params import ATTRIBUTE_CLUSTER_DNS, Inputs, TestCases
from bike.parsing.test_visitor import node

_log = logging.getLogger(__name__)
_app_label = 'app=selftest'
_client_podname = 'selftest'
_test_label = 'selftest=true'
_test_label_delete = 'selftest-'
_test_dns = 'Name:      selftest\nAddress'
_default_wait = 20

def add_prefix(prefix, text):
  return '\n'.join([prefix + l for l in text.split('\n')])


class Runner(object):
  """
  Runs the performance experiments.
  """
  def __init__(self, args):
    """
    |args| parsed command line args.
    """
    self.args = args
    self.deployment_yaml = yaml.load(open(self.args.deployment_yaml, 'r'))
    self.service_yaml = yaml.load(open(self.args.service_yaml, 'r'))
    self.client_yaml = yaml.load(open(self.args.client_yaml, 'r'))
    #self.test_params = TestCases.load_from_file(args.params)

    self.server_node = None
    self.client_node = None

    #self.db = ResultDb(self.args.db) if self.args.db else None

    #self.attributes = set()
    
    #RUN_ID = int(time.time())
    #self.attribute.set(RUN_ID)
    self.run_id = int(time.time())
    
    self.results = []

    #if self.args.use_cluster_dns:
    #  _log.info('Using cluster DNS for tests')
    #  self.args.dns_ip = '10.0.0.10'
    #  self.attributes.add(ATTRIBUTE_CLUSTER_DNS)
    
    #self.attributes.add(len(self.deployment_yaml))

    self._show_versions()

    #_log.info('DNS service IP is %s', args.dns_ip)
    _log.info('Read list of %d Nodes', len(self.deployment_yaml['nodes']))
    
    #check status of nodes - are they there and responding to ping
    self._check_nodes()
    
    
  def go(self):
    """
    Run the performance tests.
    """
    node_list = self._select_nodes()

    #test_cases = self.test_params.generate(self.attributes)
        
    #if len(test_cases) == 0:
    #  _log.warning('No test cases')
    #  return 0

    try:
      #self._ensure_out_dir(test_cases[0].run_id)
      self._ensure_out_dir(self.run_id)
      #self._reset_client()

        
      # test 1 - for each working node create a test pod
      _log.info('Running test 3...')

      for x, node in enumerate(node_list):
        try:
          self._test3(node)
          # record in result in class
          self.results[x].append('PASS')
        except Exception, e:
          _log.info('Exception caught during run, %s', e)
          fail_str = 'FAIL %s' % e
          self.results[x].append(fail_str)
          #self.results[x].append(e)

          
      #last_deploy_yaml = None
      #for test_case in test_cases:
      #  try:
      #    inputs = Inputs(self.deployment_yaml,
      #                    ['/dnsperf', '-s', self.args.dns_ip])
      #    test_case.configure(inputs)
      #    # pin server to a specific node
      #    inputs.deployment_yaml['spec']['template']['spec']['nodeName'] = \
      #        self.server_node

      #    if not self.args.use_cluster_dns and \
      #         yaml.dump(inputs.deployment_yaml) != yaml.dump(last_deploy_yaml):
      #      _log.info('Creating server with new parameters')
      #      self._teardown()
      #      self._create(inputs.deployment_yaml)
      #      self._create(self.service_yaml)
      #      self._wait_for_status(True)

      #    self._run_perf(test_case, inputs)
      #    last_deploy_yaml = inputs.deployment_yaml
      

    finally:
      self._teardown()
      #self._teardown_client()

      #if self.db is not None:
      #  self.db.commit()
      
      # write results to file
      self._write_test_data()      

    return 0

  def _kubectl(self, stdin, *args):
    """
    |return| (return_code, stdout, stderr)
    """
    cmdline = [self.args.kubectl_exec] + list(args)
    _log.debug('kubectl %s', cmdline)
    if stdin:
      _log.debug('kubectl stdin\n%s', add_prefix('in  | ', stdin))
    proc = subprocess.Popen(cmdline, stdin=PIPE, stdout=PIPE, stderr=PIPE)
    out, err = proc.communicate(stdin)
    ret = proc.wait()

    _log.debug('kubectl ret=%d', ret)
    _log.debug('kubectl stdout\n%s', add_prefix('out | ', out))
    _log.debug('kubectl stderr\n%s', add_prefix('err | ', err))

    return proc.wait(), out, err

  def _create(self, yaml_obj):
    ret, out, err = self._kubectl(yaml.dump(yaml_obj), 'create', '-f', '-')
    if ret != 0:
      _log.error('Could not create object: %d\nstdout:\n%s\nstderr:%s\n',
                 ret, out, err)
      raise Exception('create failed')
    _log.info('Create %s/%s ok', yaml_obj['kind'], yaml_obj['metadata']['name'])

  def _select_nodes(self):
    code, out, _ = self._kubectl(None, 'get', 'nodes', '-o', 'yaml')
    if code != 0:
      raise Exception('error gettings nodes: %d', code)

    nodes = [n['metadata']['name'] for n in yaml.load(out)['items']]
    _log.info('Found %d nodes in the kubernetes cluster', len(nodes))
    #print(nodes)
    # add status to this output, list found nodes, missing nodes in a table
    
    #print(n)    
    #print(n['status']['conditions'][0])
    #print(n['status']['conditions'][3])
    node_list = self.deployment_yaml['nodes']
    
    reduced_node_list = []
    
    for nm in node_list:
        reduced_node_list.append(nm.get('name','none'))
          
    found_list = []
    missing_list = []
    
    for node in nodes:
        if node in reduced_node_list:
            found_list.append([node, 'Y'])
        else:
            found_list.append([node, 'N'])
    # save results in the class
    self.results = found_list

    for node in reduced_node_list:
        if node in nodes:
            pass
        else:  # also save to the results in the class for reporting
            missing_list.append(['missing', node]) 
            self.results.append(['missing', node])
                
    
    _log.info('Matching nodes in cluster')
    
    _log.info('Missing %d nodes in cluster', len(reduced_node_list)-len(nodes))
    for n, name in enumerate(missing_list):
        _log.info('Missing item %d is %s', n+1, name[1])
        #print("Missing item {} is {}".format(n+1,name[1]))
        
    #pprint(self.results) 
    return nodes

    #nodes = [n['metadata']['name'] for n in yaml.load(out)['items']
    #         if not ('unschedulable' in n['spec'] \
    #             and n['spec']['unschedulable'])]
    
    # if checking node2node then we need more than 2 working nodes
    
    #if len(nodes) < 2:
    #  raise Exception('you need 2 or more worker nodes to run the perf test')

    #_log.info('Server node is %s', self.server_node)

  def _check_nodes(self):
    
    ret_code = []
    node_names = self.deployment_yaml['nodes']
    for node_name in node_names:
        ret_code.append(subprocess.call(['ping', '-c', '2', '-W', '1', node_name['name']],
                                        stdout=open(os.devnull, 'w'),
                                        stderr=open(os.devnull, 'w')))
        if ret_code[-1] == 0:
            _log.info('Node %s is UP', node_name['name'])
        else:
            _log.info('Node %s is DOWN', node_name['name'])
            
    return ret_code


  def _show_versions(self):
    
    code, out, _ = self._kubectl(None, 'version', '--short')
    if code != 0:
      raise Exception('error check kubectl is working: %d', code)
    _log.info('Kube versions:\n%s', out)
    #print(yaml.load(out).get("Client Version", "none"))
    #for key, val in yaml.load(out).items():  
    #    print(key, val)
    
    #versions = yaml.load(out)
    #for version in versions:
    #    v = versions[version]
    #    print(v)
         

  def _teardown(self):
    _log.info('Starting server teardown')

    #self._kubectl(None, 'delete', 'deployments', '-l', _app_label)
    self._kubectl(None, 'delete', 'pods', '-l', _app_label)
    self._kubectl(None, 'delete', 'services', '-l', _app_label)
    
    self._kubectl(None, 'label', 'nodes', '--all', _test_label_delete)
    
    self._wait_for_status(False)

    _log.info('Server teardown ok')


  def _reset_client(self):
    self._teardown_client()

    self.client_yaml['spec']['nodeName'] = self.client_node

    self._create(self.client_yaml)
    while True:
      code, _, _ = self._kubectl(None, 'get', 'pod', _client_podname)
      if code == 0:
        break
      _log.info('Waiting for client pod to start on %s', self.client_node)
      time.sleep(1)
    _log.info('Client pod to started on %s', self.client_node)

    while True:
      code, _, _ = self._kubectl(
          None, 'exec', '-i', _client_podname, '--', 'echo')
      if code == 0:
        break
      time.sleep(1)
    _log.info('Client pod ready for execution')
    self._copy_query_files()


  def _copy_query_files(self):
    _log.info('Copying query files to client')
    tarfile_contents = subprocess.check_output(
        ['/bin/tar', '-czf', '-', self.args.query_dir])
    code, _, _ = self._kubectl(
        tarfile_contents,
        'exec', '-i', _client_podname, '--', 'tar', '-xzf', '-')
    if code != 0:
      raise Exception('error copying query files to client: %d' % code)
    _log.info('Query files copied')


  def _teardown_client(self):
    _log.info('Starting client teardown')
    self._kubectl(None, 'delete', 'pod/kube-dns-perf-client')

    while True:
      code, _, _ = self._kubectl(None, 'get', 'pod', _client_podname)
      if code != 0:
        break
      time.sleep(1)
      _log.info('Waiting for client pod to terminate')

    _log.info('Client teardown complete')


  def _wait_for_status(self, active):
    while True:
      code, out, err = self._kubectl(
          None, 'get', '-o', 'yaml', 'pods', '-l', _app_label)
      if code != 0:
        _log.error('Error: stderr\n%s', add_prefix('err | ', err))
        raise Exception('error getting pod information: %d', code)
      pods = yaml.load(out)

      _log.info('Waiting for server to be %s (%d pods active)',
                'up' if active else 'deleted',
                len(pods['items']))

      if (active and len(pods['items']) > 0) or \
         (not active and len(pods['items']) == 0):
        break

      time.sleep(1)

    #if active:
    #  while True:
    #    code, out, err = self._kubectl(
    #        None,
    #        'exec', _client_podname, '--',
    #        'dig', '@' + self.args.dns_ip,
    #        'kubernetes.default.svc.cluster.local.')
    #    if code == 0:
    #      break

    #    _log.info('Waiting for DNS service to start')

    #    time.sleep(1)

    #  _log.info('DNS is up')


  def _wait_for_ready(self):
    wait_timeout = _default_wait
    while True:
      code, out, err = self._kubectl(
          None, 'get', '-o', 'yaml', 'pods', '-l', _app_label)
      if code != 0:
        _log.error('Error: stderr\n%s', add_prefix('err | ', err))
        raise Exception('error getting pod information: %d', code)
      pods = yaml.load(out)

      _log.info('Waiting for server to be %s (%d pods active)',
                'up',
                len(pods['items']))

      ready = [n['status'] for n in pods['items']]
      if (len(pods['items']) > 0 and ready[0].get('phase', None) == 'Running'):
        return True
      elif wait_timeout == 0:
        return False
      
      time.sleep(1)
      wait_timeout-=1


  def _ensure_out_dir(self, run_id):
    rundir_name = 'run-%s' % run_id
    rundir = os.path.join(self.args.out_dir, rundir_name)
    latest = os.path.join(self.args.out_dir, 'latest')

    if not os.path.exists(rundir):
      os.makedirs(rundir)
      _log.info('Created rundir %s', rundir)

    if os.path.exists(latest):
      os.unlink(latest)
    os.symlink(rundir_name, latest)

    _log.info('Updated symlink %s', latest)

    
  def _test1(self, node_name):
    _log.info('Testing Node %s', node_name)
    #add label to node
    code, out, _ = self._kubectl(None, 'label', 'node', node_name, _test_label)
    if code != 0:
      raise Exception('_test1 error labeling nodes: %d', code)

    #create service
    self._create(self.service_yaml)
    #create pod
    self._create(self.client_yaml)
    #run test
    if not self._wait_for_ready():
        raise Exception('_test1 container not Ready')
    
    code, out, _ = self._kubectl(None, 'exec', _client_podname, '--', 'nslookup', 'selftest')
    if _test_dns not in out:
      raise Exception('_test1 error dns failed: %d', code)
    
    #delete pod and service
    self._teardown()
    
    #delete label
    code, out, _ = self._kubectl(None, 'label', 'node', node_name, _test_label_delete)
    if code != 0:
      raise Exception('_test1 error de-labeling nodes: %d', code)
    
    return  


  def _test2(self, node_name):
    _log.info('Testing Node %s', node_name)
    code, out, _ = self._kubectl(None, 'exec', _client_podname, '--', 'nslookup', 'selftest')
    if _test_dns not in out:
      raise Exception('_test2 error dns failed: %d', code)
    
    return  

  def _test3(self, node_name):
      code, out, err = self._kubectl(
          None, 'get', '-o', 'yaml', 'pods', '-n', 'kube-system')
      if code != 0:
        _log.error('Error: stderr\n%s', add_prefix('err | ', err))
        raise Exception('error getting pod information: %d', code)
      pods = yaml.load(out)

      for x in pods['items']:
        if 'kube-dns' in x['metadata']['name'] and x['spec']['nodeName'] == node_name and x['status']['phase'] == 'Running':
          return True
      
      return False


  def _write_test_data(self):
    output_file = '%s/run-%s/result-%s.out' % \
      (self.args.out_dir, self.run_id, _client_podname)
    _log.info('Writing to output file %s', output_file)
        
    with open(output_file, 'w') as fh:
      results = {}
      #results['data'] = {}
      
      for key, value in enumerate(self.results):
          #results['data'][key] = value
          results[key] = value
      fh.write(yaml.dump(results))
