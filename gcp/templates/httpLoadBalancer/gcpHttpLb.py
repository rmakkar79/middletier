"""Creates http load balancer with un managed instance group """


def GenerateConfig(context):
  """Generate YAML resource configuration."""
  lb_port = context.properties['lb_port']
  
  
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
      'name': name + '-hc',
      'type': 'compute.v1.httpHealthCheck',
      'properties': {
          'name': name + '-hc',
          'port': context.properties['port'],
          'requestPath': '/_ah/health'
      }
  },
  {
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
      'name': name + '-urlmap',
      'type': 'compute.v1.urlMaps',
      'properties': {
          'name' : name + '-url-map',
          'defaultService': '$(ref.' + name + '-bes.selfLink)'
          
      }
  },
  {
      'name': name + '-tp',
      'type': 'compute.v1.targetHttpProxies',
      'properties': {
          'name' : name + '-target-proxy',
          'urlMap' : '$(ref.' + name + '-urlmap.selfLink)'
      }
  },
   {
      'name': name + '-sslcerts',
      'type': 'compute.v1.sslCertificate',
      'properties': {          
          'certificate' : "-----BEGIN CERTIFICATE-----\nMIIDbDCCAlQCCQDfZfjJKleCVjANBgkqhkiG9w0BAQUFADB4MQswCQYDVQQGEwJV\nUzELMAkGA1UECAwCQ0ExEDAOBgNVBAcMB0xham9sbGExDTALBgNVBAoMBHRlc3Qx\nDTALBgNVBAsMBHRlc3QxFDASBgNVBAMMC2V4YW1wbGUuY29tMRYwFAYJKoZIhvcN\nAQkBFgdyQHIuY29tMB4XDTE5MTAwODE2MjI1NFoXDTIwMTAwNzE2MjI1NFoweDEL\nMAkGA1UEBhMCVVMxCzAJBgNVBAgMAkNBMRAwDgYDVQQHDAdMYWpvbGxhMQ0wCwYD\nVQQKDAR0ZXN0MQ0wCwYDVQQLDAR0ZXN0MRQwEgYDVQQDDAtleGFtcGxlLmNvbTEW\nMBQGCSqGSIb3DQEJARYHckByLmNvbTCCASIwDQYJKoZIhvcNAQEBBQADggEPADCC\nAQoCggEBALmXU6gjtMTmmB2JSuIfZq6s6PY2/gXPV92ssa+0HrBiipN6S8fmXQJt\ngzDjtC4KhBnJGCnGcwZKEd9szY3D3qCNSUc8dU7wkEx9/X36ugJePQfto9gWrmXS\n9xCJ/N9o5fDZCZ+jFSlvOYFGvTpLzZtts5cPutuFqTbapYPgJUld8JJu0QJkqnD3\nfnCBIERq8KPUPzvH30inFhJI7SuIHRSAUzVfnO88EvVuXiWcMeXCpHVbnUkmEcW6\nZXRI1WbLx7rm0Ux/snQsBYL91DTDZnGsJcMw4xH7uUhp5ERSQwEuqGj1CMnfJiBn\nv+Cf9BVqfZm0E7kl7g8g4NpbDUMdYX8CAwEAATANBgkqhkiG9w0BAQUFAAOCAQEA\nWl6mpChEJGs9XR3C5aCTHcZUM3KT87Vc96xnJM2NZKn8BVgdKgomQP/xW/dbzBYg\nYpP4ijN9YCqaMdMj2HDXGFf1dkoriMmw/ZV9kTK0RL7db4WhECcUkPvIZ7Fy0gJu\nsyzNbkFAYwAunAUJFl7GHKXqAS/PAn9lwjOJUQQhD1n51m4AEjx8XeGy01nK5o0S\nqrfsADaWnI5FLZJSOo/GSDe0lEl0Q9xyJUC1XHrfPiJmBa0f2l37dQkUgyGqkZIi\nviTqBTpq1B8HMgTKfNH8z2+twnOSP2VULEMjeLrssRg4Clmgzep+ajCbeyp050EX\nUoD8hDurkxDFA3d1l3U4Mw==\n-----END CERTIFICATE-----",
          'privateKey' : "-----BEGIN RSA PRIVATE KEY-----\nMIIEpAIBAAKCAQEAuZdTqCO0xOaYHYlK4h9mrqzo9jb+Bc9X3ayxr7QesGKKk3pL\nx+ZdAm2DMOO0LgqEGckYKcZzBkoR32zNjcPeoI1JRzx1TvCQTH39ffq6Al49B+2j\n2BauZdL3EIn832jl8NkJn6MVKW85gUa9OkvNm22zlw+624WpNtqlg+AlSV3wkm7R\nAmSqcPd+cIEgRGrwo9Q/O8ffSKcWEkjtK4gdFIBTNV+c7zwS9W5eJZwx5cKkdVud\nSSYRxbpldEjVZsvHuubRTH+ydCwFgv3UNMNmcawlwzDjEfu5SGnkRFJDAS6oaPUI\nyd8mIGe/4J/0FWp9mbQTuSXuDyDg2lsNQx1hfwIDAQABAoIBAQCf7/daKRs5rHde\nzNhJskHtOnmw5YdYPm08Tfz6rEDeRK2jlnsEFFQHKZUrZq/6FXnuNsyqA6lQvDhW\n0Q77otaSie+igkmd89aG9PSlwpLWQ5xY3sSaDkHQ4lOkXyYa6e1u97tBZWtxP7bQ\n38NnH7hav9lKz3V6hN9ktFx7H4lChUdcYDHdvcbpsxhtOkV1RPVZdpprSprmxqDq\nTLBTQ/I54AIyxj19JqebR+HQO8SC0Vj6wu4DzKCKzO5aqbUBiW4cesbutbdCKpFy\niq2UGciwBGVrwf2+AakqMKX4oR5H7YGnMfk/GzIbecUDT8npQca3dWwMDe9Bo5Zr\nT4RiR9wRAoGBAOu0ul8rhid0RDxLLGLjnkYe6QvXgiShyk7SHrAD4tMabROVz876\nRpam5GtTy6Kntxo4AmMyW7XL44hQgqnKeA88PIHdleszxLbLdSI1uVuaCG7Z8SKZ\ngqGBuqEOIbJr4ePDk4pIXNgBX8GF/15r/uhX/oNZ9850KYGRLUt72hUtAoGBAMmS\nAEa7uD5KkphLKHhNICEOttbOc6ByQfD+MoNJHTo/wqya2tH1Hxe5wjHg5ss1NPYJ\nZ12TultvQfw+x6ZHb5k/Gmqowc8MZUv0vAOw1+N4zPcH0gswMlmCtBWrhOyJ5X8C\nyw9EgWJQ6Pgjpo2gAv6nxtz1leh9OksVeoZYlNTbAoGAf3m64gW0BFqJHOK7GrBn\nxRyqhVEEfbNSqtZQ6njvj6RXIaSAQzxwOMIB/1nOZCW4jWGFSQjPOL8QS4TfZdyu\nme7F+qZQkmfpF8NpkhrkKHph3THZjBDh6V80BC6UYt6dyITZoowISnpTw2Io/nQB\n5L7SU0+xCeMhH4XYrV5KT/ECgYBo659LMjEv818k+JIjNHoR2vffDe1vyal7SMWA\nQtF83W12rNBT01SQ4/cqQVfA1HwxySlNszSgnWPqab9AVRTI3ujgNeFT5a7gf45S\nGX32gI2n1CFIA5lhsEAOu43gFdMoborF8rGqPFVXvC7Yrz5/0VMY9phGQNDT/mUd\ngwRNWwKBgQC+j4nGCPjW/gocrHc/RZG2pS09Y6rXIu/c6W6nPk4fRUIY3Q8Wd9Uf\n2AM3Tc9bwlxPVS2a2UDlRpBPIF72Psb40oUncX/uB/xmYScW9arYc5HqyatTzXmH\ncdT7uZ53Hu55JztbRIk6yUWQDWKENHYnPQv3XjTHI6lkNT+U+jrJ5A==\n-----END RSA PRIVATE KEY-----"
      }
  },
  {
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