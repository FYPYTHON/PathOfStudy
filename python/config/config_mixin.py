#!python3
# coding=utf-8


class SectionDiffMixin(object):
    def __init__(self):
        self.diff_section = set()

    def set_diff_section(self, diff_section):
        """
        eg: {"rmq:port", "redis:password"...}
        :param diff_section:  set
        """
        self.diff_section = diff_section

    def get_diff_key(self, section, key=None):
        if key is not None:
            cur_sec = "{}:{}".format(section, key)
        else:
            cur_sec = section
        isKeyDiff = False
        for sec_info in self.diff_section:
            if cur_sec in sec_info:
                isKeyDiff = True
                break
        return isKeyDiff


def test():
    t_diff_section = {'rabbitmq:ha_port', 'rabbitmq:port', 'dms:gossip_port', 'rabbitmq:ha_manager_port', 'gaussdb:ha_port', 'mha:port', 'dms:check_port', 'dms:rpc_port', 'dms:grpc_port', 'gaussdb:port', 'gaussdb:manager_port', 'rabbitmq:erl_epmd_port', 'rabbitmq:manager_port', 'redis:port', 'common:type', 'redis:ha_port', 'gaussdb:heartbeatport', 'zookeeper'}
    diff_mixin = SectionDiffMixin()
    diff_mixin.set_diff_section(t_diff_section)
    res = diff_mixin.get_diff_key('rabbitmq', 'port')
    print(res)


if __name__ == '__main__':
    test()
    exit(1)
