import boto3
from botocore.config import Config
from dotenv import dotenv_values

config = dotenv_values(".env")

DRY_RUN = int(config.get('DRY_RUN'))
my_config = Config(
    region_name=config.get('REGION')
)

_client = boto3.client('ec2',
                       aws_access_key_id=config.get('AWS_ACCESS_KEY_ID'),
                       aws_secret_access_key=config.get('AWS_SECRET_ACCESS_KEY'),
                       region_name=config.get('REGION'))
ec2 = boto3.resource("ec2", config=my_config)

boto3.set_stream_logger('')


def crear_instancia():
    instance = ec2.create_instances(
        InstanceType='t2.micro',
        Monitoring={
            'Enabled': True
        },
        MinCount=1,
        MaxCount=1,
        DryRun=bool(DRY_RUN),
        SecurityGroupIds=[
            'sg-0e5842b06c8ed87f8',
        ],
        EbsOptimized=True,
        InstanceInitiatedShutdownBehavior='stop',
        
        LaunchTemplate={
            'LaunchTemplateId': '0e7478d2842766243',
            'Version': '1'
        }
    )

    return instance


def eliminar_instancia(instance_id):
    response = ec2.terminate_instances(
        InstanceIds=[
            instance_id,
        ],
        DryRun=DRY_RUN
    )
    return response


def iniciar_instancia(instance_id):
    response = ec2.start_instances(
        InstanceIds=[
            instance_id,
        ],
        DryRun=DRY_RUN
    )
    return response


def detener_instancia(instance_id):
    response = ec2.stop_instances(
        InstanceIds=[
           instance_id,
        ],
        Hibernate=False,
        DryRun=DRY_RUN,
        Force=True
    )


def reiniciar_instancia(instance_id) -> None:
    ec2.reboot_instances(
        InstanceIds=[
            instance_id,
        ],
        DryRun=DRY_RUN
)
