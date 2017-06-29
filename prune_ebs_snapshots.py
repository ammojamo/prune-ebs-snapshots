#!/usr/bin/env python

# @copyright: James Watmuff (c) 2017. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Prune EBS Snapshots based on a simple backup retention policy

configuration
-------------

This script uses the boto3 library to communicate with AWS. You must configure your AWS credentials using one
of the methods supported by boto3. For full details see:

https://boto3.readthedocs.io/en/latest/guide/configuration.html#guide-configuration

The AWS user must have appropriate permissions. Here is an example AWS policy:

	{
		"Version": "2012-10-17",
		"Statement": [
			{
				"Sid": "Stmt1422916495000",
				"Effect": "Allow",
				"Action": [
					"ec2:DeleteSnapshot",
					"ec2:DescribeSnapshots"
				],
				"Resource": [
					"*"
				]
			}
		]
	}

usage
-----

Always use the ``--help`` option to see the most up-to-date options available.

Basic usage is:

	prune-ebs-snapshots [options] volume_id tag_name tag_value

``volume_id`` specifies which EBS volume to prune snapshots for

``tag_name`` and ``tag_value`` specify a tag and corresponding value that must be present on all snapshots considered for pruning.
Typically you would configure a backup script to include this particular tag value on all snapshots created for backup purposes.
Snapshots created for other purposes would not have this tag, and therefore would not be deleted by this pruning script, or considered
as part of the backup set for determining which snapshots to delete.

Options are used to specify how many daily, weekly, monthly and yearly snapshots to retain. Use ``--help`` for more details.

"""

import boto3
import sys
import argparse
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import pytz

__author__ = 'James Watmuff'
__email__ = 'james.watmuff@gmail.com'


def main():
	parser = argparse.ArgumentParser(description='Prunes EBS snapshots')
	parser.add_argument('volume_id', type=str, help='EBS Volume ID')
	parser.add_argument('tag_name', type=str, help='Snapshot tag value')
	parser.add_argument('tag_value', type=str, help='Snapshot tag name')

	parser.add_argument('--daily', type=int, help='Number of daily snapshots to keep')
	parser.add_argument('--weekly', type=int, help='Number of weekly snapshots to keep')
	parser.add_argument('--monthly', type=int, help='Number of monthly snapshots to keep')
	parser.add_argument('--yearly', type=int, help='Number of yearly snapshots to keep')

	parser.add_argument('--dry-run', '-n', dest='dry_run', action='store_true', help='Dry run - print actions that would be taken')

	args = parser.parse_args()

	ec2 = boto3.resource('ec2')

	filters = [
		{ 'Name': 'volume-id', 'Values': [args.volume_id] },
		{ 'Name': 'tag:' + args.tag_name, 'Values': [ args.tag_value ]},
		{ 'Name': 'status', 'Values': [ 'completed' ]}
	]

	snapshots = sorted([(s.start_time, s.id) for s in ec2.snapshots.filter(Filters=filters)])

	snapshots_to_keep = set()

	now = datetime.now(pytz.utc)

#	def two(x):
#		return (x,x)

#	snapshots = sorted([two(now - timedelta(days = x)) for x in range(0,50)] + [two(now - relativedelta(months = x)) for x in range(0,50)])

	if args.daily != None:
		update_snapshots(snapshots_to_keep, snapshots, start_of_day, now - timedelta(days = args.daily), now)

	if args.weekly != None:
		update_snapshots(snapshots_to_keep, snapshots, start_of_week, now - timedelta(weeks = args.weekly), now)

	if args.monthly != None:
		update_snapshots(snapshots_to_keep, snapshots, start_of_month, now - relativedelta(months = args.monthly), now)

    if args.yearly != None:
            update_snapshots(snapshots_to_keep, snapshots, start_of_year, now - relativedelta(years = args.yearly), now)

	snapshots_to_delete = sorted(set(snapshots) - snapshots_to_keep)

	if args.dry_run:
		for s in snapshots:
			if s in snapshots_to_keep:
				print "KEEP %s" % s[1]
			else:
				print "DELETE %s" % s[1]
		if len(snapshots) == 0:
			print "Nothing to do"
		return


	for snapshot in snapshots_to_delete:
		snapshot.delete()

def start_of_week(date):
	return date.replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days = date.weekday())

def start_of_day(date):
	return date.replace(hour=0, minute=0, second=0, microsecond=0)

def start_of_month(date):
	return date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

def start_of_year(date):
	return date.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)

def update_snapshots(snapshots_to_keep, snapshots, period_start, cutoff_date, now):
	prev = None
	for s in snapshots:
		snapshot_time = s[0]
		curr = period_start(snapshot_time)
		if curr != prev and (snapshot_time > cutoff_date or cutoff_date > now):
			snapshots_to_keep.add(s)
		prev = curr

if __name__ == "__main__":
	sys.exit(main())
