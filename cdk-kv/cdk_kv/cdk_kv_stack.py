import os
from aws_cdk import core as cdk

# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import core
from aws_cdk import (core, aws_ec2 as ec2, aws_ecs as ecs,
                     aws_ecs_patterns as ecs_patterns)
import aws_cdk.aws_codepipeline as codepipeline
import aws_cdk.aws_codebuild as codebuild
import aws_cdk.aws_codepipeline_actions as codepipeline_actions
from aws_cdk.aws_elasticloadbalancingv2 import IpAddressType
from aws_cdk.core import SecretValue
import aws_cdk.aws_ecr as ecr
import aws_cdk.aws_iam as iam            

class CdkKvStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        gh_token  = os.environ.get("GITHUB_TOKEN")
        gh_owner = os.environ.get("GITHUB_OWNER")
        gh_repo_name = os.environ.get("GITHUB_REPO_NAME")
        account_id = os.getenv('CDK_DEFAULT_ACCOUNT')
        region = os.getenv('CDK_DEFAULT_REGION')
        
        kv_repo = ecr.Repository(self, "kv-repo")

        kv_vpc = ec2.Vpc(self, "KvVpc", max_azs=3)
        
        kv_cluster = ecs.Cluster(self, "KvEcsCluster", vpc=kv_vpc)
        
        kv_ecsservice = ecs_patterns.ApplicationLoadBalancedFargateService(self, "KVappFargateService",
            cluster=kv_cluster,            
            cpu=256,
            desired_count=1,
            assign_public_ip=True,
            task_image_options=ecs_patterns.ApplicationLoadBalancedTaskImageOptions(
                image=ecs.ContainerImage.from_registry("amazon/amazon-ecs-sample")),
            memory_limit_mib=512,
            public_load_balancer=True
            )
        
        kv_repo_policy = iam.PolicyStatement(actions=["ecr:BatchCheckLayerAvailability",
                                     "ecr:BatchGetImage", "ecr:GetDownloadUrlForLayer"],
                            resources=[kv_repo.repository_arn])

        kv_ecr_policy = iam.PolicyStatement(actions=["ecr:GetAuthorizationToken"], resources=["*"])

        kv_ecsservice.service.task_definition.add_to_execution_role_policy(kv_repo_policy)
        kv_ecsservice.service.task_definition.add_to_execution_role_policy(kv_ecr_policy)

        taskdef_arn = kv_ecsservice.task_definition.task_definition_arn
        

        build_variables = {
            "AWS_ACCOUNT_ID": codebuild.BuildEnvironmentVariable(value=account_id),
            "AWS_DEFAULT_REGION": codebuild.BuildEnvironmentVariable(value=region),
            "IMAGE_REPO_NAME": codebuild.BuildEnvironmentVariable(value=kv_repo.repository_name),
            "IMAGE_TAG": codebuild.BuildEnvironmentVariable(value="latest"),
            "TASK_DEF": codebuild.BuildEnvironmentVariable(value=core.Arn.split(
                        arn=taskdef_arn, arn_format=core.ArnFormat.SLASH_RESOURCE_NAME).resource_name)
        }

        source_artifact = codepipeline.Artifact()
        
        build_artifact = codepipeline.Artifact()

        build = codebuild.PipelineProject(self, "KVStore-build",
                                          environment=codebuild.BuildEnvironment(privileged=True,
                                          build_image=codebuild.LinuxBuildImage.AMAZON_LINUX_2_3,
                                          environment_variables=build_variables), vpc=kv_vpc
                                          )
        build.role.add_managed_policy(policy=iam.ManagedPolicy.from_aws_managed_policy_name(
                                      managed_policy_name="AmazonEC2ContainerRegistryPowerUser"))

        
        kv_pipleine = codepipeline.Pipeline(self, "KVPipeline", pipeline_name="KVstorePipeline", restart_execution_on_update=True, 
                              stages=[
                                {
                                    "stageName": "Source",
                                    "actions": [codepipeline_actions.GitHubSourceAction(
                                        action_name="GitHub-fetch",
                                        output=source_artifact,
                                        #oauth_token=SecretValue.secrets_manager("GITHUB_TOKEN_NAME"),
                                        oauth_token=SecretValue.plain_text(gh_token),
                                        trigger=codepipeline_actions.GitHubTrigger.POLL,
                                        # Replace these with your actual GitHub project info
                                        owner=gh_owner,
                                        repo=gh_repo_name,
                                        branch="main")
                                    ],
                                },
                                {
                                    "stageName": "Build",
                                    "actions": [codepipeline_actions.CodeBuildAction(
                                        action_name="TestBuild-action",
                                        project=build,
                                        input=source_artifact,
                                        outputs=[build_artifact]
                                    )]
                                },
                                {
                                    "stageName": "Deploy",
                                    "actions": [codepipeline_actions.EcsDeployAction(
                                            action_name="ECS-Deploy",
                                            input=build_artifact,
                                            service=kv_ecsservice.service,
                                            deployment_timeout=cdk.Duration.minutes(20)
                                            )]
                                }
                              ])
