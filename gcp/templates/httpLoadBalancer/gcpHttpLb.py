"""Creates http load balancer with un managed instance group """


def GenerateConfig(context):
  """Generate YAML resource configuration."""
  lb_port = context.properties['lb_port']
  
  """ Create un managed instance group """
  name = context.env['name']
  resources = [{
      'name': name + '-ig',
      'type': 'compute.v1.instanceGroup',
      'properties': {
          'zone': context.properties['zone'],          
          'subnetwork': context.properties['ig_network_cidr']
      },
  },
  {
      """ Create health check """
      'name': name + '-hc',
      'type': 'compute.v1.httpHealthCheck',
      'properties': {
          'port': context.properties['port'],
          'requestPath': '/_ah/health'
      }
  },
  {
      """ Create backend service and attach instance group """
      'name': name + '-bes',
      'type': 'compute.v1.backendService',
      'properties': {
          'port': context.properties['port'],          
          'portName': context.properties['service'],
          'backends': [{
              'name': name + '-primary',
              'group': '$(ref.' + name + '-ig.selfLink)'
          }],
          'healthChecks': ['$(ref.' + name + '-hc.selfLink)']
      }
  },
  {
      """ Create URL map """
      'name': name + '-urlmap',
      'type': 'compute.v1.urlMaps',
      'properties': {
          'name' : name + '-url-map',
          'defaultService': '$(ref.' + name + '-bes.selfLink)'
          
      }
  },
  {
      """ Create http proxy and attach url map to it """
      'name': name + '-tp',
      'type': 'compute.v1.targetHttpProxies',
      'properties': {
          'name' : name + '-target-proxy',
          'urlMap' : '$(ref.' + name + '-urlmap.selfLink)'
      }
  },
  {
       """ Create loadbalancer and attach http proxy to it """
      'name': name + '-lb',
      'type': 'compute.v1.globalForwardingRule',
      'properties': {
          'IPProtocol': 'TCP',
          'portRange': lb_port,
          'name': 'firstloadb',                    
          'target': '$(ref.' + name + '-tp.selfLink)'
      }
  },
    {
         """ Make a api call to add instance to un managed instance group """
        'name': name + '-ig-members',
        'action': 'gcp-types/compute-v1:compute.instanceGroups.addInstances',
        'properties': {
            'project': context.properties['project_id'],
            'zone' : context.properties['zone'],
            'instanceGroup': 'frontend-ig',
            "instances": [
    {
      "instance": 'projects/' + context.properties['project_id'] + '/zones/' + context.properties['zone'] + '/instances/' + context.properties['instance']
    }
  ]            
        }
    }
  ]
  return {'resources': resources}