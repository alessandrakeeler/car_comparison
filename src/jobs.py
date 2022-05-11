import json
import os
import uuid
from flask import Flask, request
import redis
from hotqueue import HotQueue


#redis_ip = os.environ.get('REDIS_IP')
#if not redis_ip:
 #   raise Exception()
redis_ip = '127.0.0.1'
rd = redis.Redis(host='127.0.0.1', port=6413, db=0)
q = HotQueue("queue", host=redis_ip, port=6413, db=1)
jdb = redis.Redis(host=redis_ip, port=6413, db=2, decode_responses=True)
img_db = redis.Redis(host=redis_ip, port=6413, db=3)

def _generate_jid():
    """
    Generate a pseudo-random identifier for a job.
    """
    return str(uuid.uuid4())

def _generate_job_key(jid):
    """
    Generate the redis key from the job id to be used when storing, retrieving or updating
    a job in the database.
    """
    return 'job.{}'.format(jid)

def _instantiate_job(jid, status, feature1, feature2, comparison_factor):
    """
    Create the job object description as a python dictionary. Requires the job id, status,
    feature1, feature2, and comparison parameters 
    """
    if type(jid) == str:
        return {'id': jid,
                'status': status,
                'feature1': feature1,
                'feature2': feature2, 
                'comparison_factor' : comparison_factor
               }
    return {'id': jid.decode('utf-8'),
            'status': status.decode('utf-8'),
            'feature1': feature1.decode('utf-8'),
            'feature2': feature2.decode('utf-8')
            'comparison_factor': comparison_factor.decode('utf-8')
           }

def _save_job(job_key, job_dict):
    """Save a job object in the Redis database."""
    jdb.hset(job_key, mapping=job_dict)
    return

def _queue_job(jid):
    """Add a job to the redis queue."""
    q.put(jid)
    return


def add_job(feature1, feature2, comparison_fator, status="submitted"):
    """Add a job to the redis queue."""
    jid = _generate_jid()
    job_dict = _instantiate_job(jid, status, feature1, feature2, comparison_factors)
    _save_job(_generate_job_key(jid), job_dict)
    _queue_job(jid)
    return job_dict

def get_job_by_id(jid):
    """Return job dictionary given jid"""
    return (jdb.hgetall(_generate_job_key(jid).encode('utf-8')))

def update_job_status(jid, status):
    """Update the status of job with job id `jid` to status `status`."""
    job = get_job_by_id(jid)
    if job:
        job['status'] = status
        _save_job(_generate_job_key(jid), job)

    else:
        raise Exception()