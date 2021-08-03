import os
from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import (core, aws_ec2 as ec2, aws_ecs as ecs,
                     aws_ecs_patterns as ecs_patterns)
import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_codepipeline_actions as codepipeline_actions
from aws_cdk.aws_elasticloadbalancingv2 import IpAddressType
from aws_cdk.core import SecretValue
import aws_cdk.aws_ecr as ecr
import aws_cdk.aws_iam as iam            

class CdkKvPipelineStack(cdk.NestedStack):

    def __init__(self, scope: cdk.Construct, construct_id: str, kv_ecstaskdef: ecs.FargateTaskDefinition,
                 kv_pipleine: codepipeline.Pipeline, kv_cluster: ecs.Cluster, build_artifact: codepipeline.Artifact, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        kv_ecsservice = ecs_patterns.ApplicationLoadBalancedFargateService(self, "KVappFargateService",
            cluster=kv_cluster,            
            cpu=256,
            desired_count=1,
            assign_public_ip=True,
            #task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(image=ecs.ContainerImage.from_ecr_repository(kv_repo)),
            memory_limit_mib=512,
            public_load_balancer=True,
            task_definition=kv_ecstaskdef,
            circuit_breaker=ecs.DeploymentCircuitBreaker(rollback=True))

        kv_deploy_action = codepipeline_actions.EcsDeployAction(
                                            action_name="ECS-Deploy",
                                            input=build_artifact,
                                            service=kv_ecsservice.service,
                                            deployment_timeout=cdk.Duration.minutes(20)
                            )
        
        
        kv_pipleine.add_stage(
            stage_name = "Deploy",
            actions= [kv_deploy_action])