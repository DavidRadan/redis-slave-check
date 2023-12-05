#!/usr/bin/python

# Redis Slave Connectivity Check
# Ugur Engin
# 12 August, 2016

# added support for password and both python 2/3 supported ( tested with rocky linux 9.2)
# ./check_redis_slave.py -H 127.0.0.1 -P 6379 -p PASSWORD
#OUTPUT :  OK: slave redis is connected properly to the master|master_last_io_seconds_ago=0;0;0;0


from optparse import OptionParser
import os, sys, redis, json

parser = OptionParser()
parser.add_option("-H", dest="host", type='string',
                  help="Slave redis host address")
parser.add_option("-P", dest="port", type='int',
                  help="Redis tcp port, default 6379", default='6379')
parser.add_option("-p", dest="password", type='string',
                  help="Redis password, default None", default=None)
(options, args) = parser.parse_args()

def check_req():
    if not options.host:
        print("Unknown: Host address is required.")
        raise SystemExit(3)
    elif options.port is None:
        options.port = 6379
    elif sys.platform.startswith('linux'):
        try:
            import redis
        except ImportError as e:
            print("python redis module doesn't exist")
            pass

if __name__ == '__main__':
    check_req()

    def conn_redis():
        try:
            if options.password:
                conn = redis.StrictRedis(options.host, options.port, db=0, password=options.password)
            else:
                conn = redis.StrictRedis(options.host, options.port, db=0)
            conn.ping()
        except redis.ConnectionError:
            print("Unknown: Redis connection is failed.")
            raise SystemExit(3)
        return conn

    def valid_redis():
        r = conn_redis()
        i = r.info()
        r_out = json.loads(json.dumps(i))
        r_role = r_out["role"]
        if r_role != 'slave':
            print('Unknown: target redis server must be a slave!')
            raise SystemExit(3)

    if __name__ == '__main__':
        valid_redis()

    def check_redis():
        r = conn_redis()
        i = r.info()
        r_out = json.loads(json.dumps(i))
        r_link = r_out["master_link_status"]
        r_iosec = r_out["master_last_io_seconds_ago"]
        if r_link != 'up' and r_iosec == -1:
            print('Critical: slave redis server has failed to connect to the master. It is down!')
            raise SystemExit(2)
        else:
            print('OK: slave redis is connected properly to the master' '' + '|' + 'master_last_io_seconds_ago=' + str(
                r_iosec) + ';0;0;0')
            raise SystemExit(0)

    if __name__ == '__main__':
        check_redis()
