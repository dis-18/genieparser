"""route.py

Linux parsers for the following commands:
    * route
"""

# python
import re

# metaparser
from genie.metaparser import MetaParser
from genie.metaparser.util.schemaengine import Schema, Any, Optional

# =======================================================
# Schema for 'route'
# =======================================================
class RouteSchema(MetaParser):
    """Schema for route"""

    # Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
    # 0.0.0.0         192.168.1.1     0.0.0.0         UG        0 0          0 wlo1

    schema = {
        Any(): {
            'destination': str,
            'gateway': str,
            'mask': str,
            'flags': str,
            Optional('metric'): int,
            Optional('ref'): int,
            Optional('use'): int,
            Optional('mss'): int,
            Optional('window'): int,
            Optional('irtt'): int,
            'interface': str
        }
    }

    schema = {
        'routes': {
            Any(): { # 'destination'
                'mask': {
                    Any(): {
                        'nexthop': {
                            Any(): { # index: 1, 2, 3, etc
                                'interface': str,
                                'flags': str,
                                'gateway': str,
                                'metric': int,
                                'ref': int,
                                'use': int
                            }
                        }
                    }
                }
            }
        }
    }

# =======================================================
# Parser for 'route'
# =======================================================
class Route(RouteSchema):
    """Parser for 
        * route
        * route -4 -n 
        * route -4n
        * route -n4
        * route -n -4
        """

    cli_command = ['route', 'route {flag}']

    def cli(self, flag=None, output=None):
        if output is None:    
            cmd = self.cli_command[0]
            if flag in ['-4 -n', '-4n', '-n4']:
                command = self.cli_command[1].replace('{flag}', flag)
            out = self.device.execute(cmd)
        else:
            out = output

        # Destination     Gateway         Genmask         Flags Metric Ref    Use Iface
        # 192.168.1.0     0.0.0.0         255.255.255.0   U     600    0        0 wlo1

        p1 = re.compile(r'(?P<destination>[a-z0-9\.\:]+)'
                        ' +(?P<gateway>[a-z0-9\.\:_]+)'
                        ' +(?P<mask>[a-z0-9\.\:]+)'
                        ' +(?P<flags>[a-zA-Z]+)'
                        ' +(?P<metric>(\d+))'
                        ' +(?P<ref>(\d+))'
                        ' +(?P<use>(\d+))'
                        ' +(?P<interface>\S+)'
                        )
        
        # Initializes the Python dictionary variable
        parsed_dict = {}

        # Defines the "for" loop, to pattern match each line of output

        for line in out.splitlines():
            line = line.strip()


            # 192.168.1.0     0.0.0.0         255.255.255.0   U     600    0        0 wlo1
            m = p1.match(line)
            if m:
                group = m.groupdict()
                destination = group['destination']
                parsed_dict.setdefault(destination, {})
                parsed_dict[destination].update({k: (int(v) if v.isdigit() else v) for k, v in group.items()})
                continue

        return parsed_dict


# =======================================================
# Parser for 'netstat -rn'
# =======================================================
class ShowNetworkStatusRoute(RouteSchema):
    """Parser for 
        * netstat -rn 
        """

    cli_command = ['netstat -rn']

    def cli(self, output=None):
        if output is None:    
            cmd = self.cli_command[0]
            out = self.device.execute(cmd)
        else:
            out = output

        # Destination     Gateway         Genmask         Flags   MSS Window  irtt Iface
        # 0.0.0.0         192.168.1.1     0.0.0.0         UG        0 0          0 enp7s0


        p1 = re.compile(r'(?P<destination>[a-z0-9\.\:]+)'
                        ' +(?P<gateway>[a-z0-9\.\:_]+)'
                        ' +(?P<mask>[a-z0-9\.\:]+)'
                        ' +(?P<flags>[a-zA-Z]+)'
                        ' +(?P<mss>(\d+))'
                        ' +(?P<window>(\d+))'
                        ' +(?P<irtt>(\d+))'
                        ' +(?P<interface>\S+)'
                        )
        
        # Initializes the Python dictionary variable
        parsed_dict = {}

        # Defines the "for" loop, to pattern match each line of output

        for line in out.splitlines():
            line = line.strip()


            # 0.0.0.0         192.168.1.1     0.0.0.0         UG        0 0          0 wlo1
            m = p1.match(line)
            if m:
                group = m.groupdict()
                destination = group['destination']
                parsed_dict.setdefault(destination, {})
                parsed_dict[destination].update({k: (int(v) if v.isdigit() else v) for k, v in group.items()})
                continue

        return parsed_dict

