Prune EBS Snapshots based on a simple backup retention policy

Configuration
-------------

This script uses the boto3 library to communicate with AWS. You must configure your AWS credentials using one
of the methods supported by boto3. For full details see:

https://boto3.readthedocs.io/en/latest/guide/configuration.html#guide-configuration

The AWS user must have appropriate permissions. Here is an example AWS policy::

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

Usage
-----

Always use the ``--help`` option to see the most up-to-date options available.

Basic usage is:

``prune-ebs-snapshots [options] volume_id tag_name tag_value``

``volume_id`` specifies which EBS volume to prune snapshots for

``tag_name`` and ``tag_value`` specify a tag and corresponding value that must be present on all snapshots considered for pruning.
Typically you would configure a backup script to include this particular tag value on all snapshots created for backup purposes.
Snapshots created for other purposes would not have this tag, and therefore would not be deleted by this pruning script, or considered
as part of the backup set for determining which snapshots to delete.

Options are used to specify how many daily, weekly, monthly and yearly snapshots to retain. Use ``--help`` for more details.
