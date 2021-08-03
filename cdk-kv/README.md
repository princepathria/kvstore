# Welcome to your KV store CDK Python project!

This project will create
* CI/CD pipeline - Github + CodeBuild + CodePipeline
* Infrastructure resources - ALB + ECS Fargate

The `cdk.json` file tells the CDK Toolkit how to execute your app.

This project is set up like a standard Python project.  The initialization
process also creates a virtualenv within this project, stored under the `.venv`
directory.  To create the virtualenv it assumes that there is a `python3`
(or `python` for Windows) executable in your path with access to the `venv`
package. If for any reason the automatic creation of the virtualenv fails,
you can create the virtualenv manually.

To manually create a virtualenv on MacOS and Linux:

```
$ python3 -m venv .venv
```

After the init process completes and the virtualenv is created, you can use the following
step to activate your virtualenv.

```
$ source .venv/bin/activate
```

If you are a Windows platform, you would activate the virtualenv like this:

```
% .venv\Scripts\activate.bat
```

Once the virtualenv is activated, you can install the required dependencies.

```
$ pip install -r requirements.txt
```
Export the following shell variables

* [Create a GitHub token for poll](https://docs.github.com/en/github/authenticating-to-github/keeping-your-account-and-data-secure/creating-a-personal-access-token)

```
GITHUB_OWNER=princepathria
GITHUB_REPO_NAME=kvstore
GITHUB_TOKEN=
CDK_DEFAULT_ACCOUNT= AWS account for deployment
CDK_DEFAULT_REGION= AWS region for deployment
```
Bootstrap your AWS account for CDK

```
$ cdk bootstrap aws://$CDK_DEFAULT_ACCOUNT/$CDK_DEFAULT_REGION
```
At this point you can now synthesize the CloudFormation template for this code.

```
$ cdk synth
```
To check what all resources are being deployed

```
$ cdk diff
Stack CdkKvStack
IAM Statement Changes
┌───┬──────────────────────────────────────────────┬────────┬──────────────────────────────────────────────┬──────────────────────────────────────────────┬───────────────────────────────────────────────┐
│   │ Resource                                     │ Effect │ Action                                       │ Principal                                    │ Condition                                     │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVPipeline/ArtifactsBucket.Arn}            │ Allow  │ s3:Abort*                                    │ AWS:${KVStore-build/Role}                    │                                               │
│   │ ${KVPipeline/ArtifactsBucket.Arn}/*          │        │ s3:DeleteObject*                             │                                              │                                               │
│   │                                              │        │ s3:GetBucket*                                │                                              │                                               │
│   │                                              │        │ s3:GetObject*                                │                                              │                                               │
│   │                                              │        │ s3:List*                                     │                                              │                                               │
│   │                                              │        │ s3:PutObject                                 │                                              │                                               │
│ + │ ${KVPipeline/ArtifactsBucket.Arn}            │ Allow  │ s3:Abort*                                    │ AWS:${KVPipeline/Role}                       │                                               │
│   │ ${KVPipeline/ArtifactsBucket.Arn}/*          │        │ s3:DeleteObject*                             │                                              │                                               │
│   │                                              │        │ s3:GetBucket*                                │                                              │                                               │
│   │                                              │        │ s3:GetObject*                                │                                              │                                               │
│   │                                              │        │ s3:List*                                     │                                              │                                               │
│   │                                              │        │ s3:PutObject                                 │                                              │                                               │
│ + │ ${KVPipeline/ArtifactsBucket.Arn}            │ Allow  │ s3:GetBucket*                                │ AWS:${KVPipeline/Deploy/ECS-Deploy/CodePipel │                                               │
│   │ ${KVPipeline/ArtifactsBucket.Arn}/*          │        │ s3:GetObject*                                │ ineActionRole}                               │                                               │
│   │                                              │        │ s3:List*                                     │                                              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVPipeline/ArtifactsBucketEncryptionKey.Ar │ Allow  │ kms:*                                        │ AWS:arn:${AWS::Partition}:iam::714289824363: │                                               │
│   │ n}                                           │        │                                              │ root                                         │                                               │
│ + │ ${KVPipeline/ArtifactsBucketEncryptionKey.Ar │ Allow  │ kms:Decrypt                                  │ AWS:${KVStore-build/Role}                    │                                               │
│   │ n}                                           │        │ kms:DescribeKey                              │                                              │                                               │
│   │                                              │        │ kms:Encrypt                                  │                                              │                                               │
│   │                                              │        │ kms:GenerateDataKey*                         │                                              │                                               │
│   │                                              │        │ kms:ReEncrypt*                               │                                              │                                               │
│ + │ ${KVPipeline/ArtifactsBucketEncryptionKey.Ar │ Allow  │ kms:Decrypt                                  │ AWS:${KVStore-build/Role}                    │                                               │
│   │ n}                                           │        │ kms:Encrypt                                  │                                              │                                               │
│   │                                              │        │ kms:GenerateDataKey*                         │                                              │                                               │
│   │                                              │        │ kms:ReEncrypt*                               │                                              │                                               │
│ + │ ${KVPipeline/ArtifactsBucketEncryptionKey.Ar │ Allow  │ kms:Decrypt                                  │ AWS:${KVPipeline/Role}                       │                                               │
│   │ n}                                           │        │ kms:DescribeKey                              │                                              │                                               │
│   │                                              │        │ kms:Encrypt                                  │                                              │                                               │
│   │                                              │        │ kms:GenerateDataKey*                         │                                              │                                               │
│   │                                              │        │ kms:ReEncrypt*                               │                                              │                                               │
│ + │ ${KVPipeline/ArtifactsBucketEncryptionKey.Ar │ Allow  │ kms:Decrypt                                  │ AWS:${KVPipeline/Deploy/ECS-Deploy/CodePipel │                                               │
│   │ n}                                           │        │ kms:DescribeKey                              │ ineActionRole}                               │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVPipeline/Build/TestBuild-action/CodePipe │ Allow  │ sts:AssumeRole                               │ AWS:arn:${AWS::Partition}:iam::714289824363: │                                               │
│   │ lineActionRole.Arn}                          │        │                                              │ root                                         │                                               │
│ + │ ${KVPipeline/Build/TestBuild-action/CodePipe │ Allow  │ sts:AssumeRole                               │ AWS:${KVPipeline/Role}                       │                                               │
│   │ lineActionRole.Arn}                          │        │                                              │                                              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVPipeline/Deploy/ECS-Deploy/CodePipelineA │ Allow  │ sts:AssumeRole                               │ AWS:arn:${AWS::Partition}:iam::714289824363: │                                               │
│   │ ctionRole.Arn}                               │        │                                              │ root                                         │                                               │
│ + │ ${KVPipeline/Deploy/ECS-Deploy/CodePipelineA │ Allow  │ sts:AssumeRole                               │ AWS:${KVPipeline/Role}                       │                                               │
│   │ ctionRole.Arn}                               │        │                                              │                                              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVPipeline/Role.Arn}                       │ Allow  │ sts:AssumeRole                               │ Service:codepipeline.amazonaws.com           │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVStore-build.Arn}                         │ Allow  │ codebuild:BatchGetBuilds                     │ AWS:${KVPipeline/Build/TestBuild-action/Code │                                               │
│   │                                              │        │ codebuild:StartBuild                         │ PipelineActionRole}                          │                                               │
│   │                                              │        │ codebuild:StopBuild                          │                                              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVStore-build/Role.Arn}                    │ Allow  │ sts:AssumeRole                               │ Service:codebuild.amazonaws.com              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVappFargateService/TaskDef/ExecutionRole. │ Allow  │ sts:AssumeRole                               │ Service:ecs-tasks.amazonaws.com              │                                               │
│   │ Arn}                                         │        │                                              │                                              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVappFargateService/TaskDef/TaskRole.Arn}  │ Allow  │ sts:AssumeRole                               │ Service:ecs-tasks.amazonaws.com              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVappFargateService/TaskDef/web/LogGroup.A │ Allow  │ logs:CreateLogStream                         │ AWS:${KVappFargateService/TaskDef/ExecutionR │                                               │
│   │ rn}                                          │        │ logs:PutLogEvents                            │ ole}                                         │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${kv-repo.Arn}                               │ Allow  │ ecr:BatchCheckLayerAvailability              │ AWS:${KVappFargateService/TaskDef/ExecutionR │                                               │
│   │                                              │        │ ecr:BatchGetImage                            │ ole}                                         │                                               │
│   │                                              │        │ ecr:GetDownloadUrlForLayer                   │                                              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ *                                            │ Allow  │ ecr:GetAuthorizationToken                    │ AWS:${KVappFargateService/TaskDef/ExecutionR │                                               │
│   │                                              │        │                                              │ ole}                                         │                                               │
│ + │ *                                            │ Allow  │ ec2:CreateNetworkInterface                   │ AWS:${KVStore-build/Role}                    │                                               │
│   │                                              │        │ ec2:DeleteNetworkInterface                   │                                              │                                               │
│   │                                              │        │ ec2:DescribeDhcpOptions                      │                                              │                                               │
│   │                                              │        │ ec2:DescribeNetworkInterfaces                │                                              │                                               │
│   │                                              │        │ ec2:DescribeSecurityGroups                   │                                              │                                               │
│   │                                              │        │ ec2:DescribeSubnets                          │                                              │                                               │
│   │                                              │        │ ec2:DescribeVpcs                             │                                              │                                               │
│ + │ *                                            │ Allow  │ ecs:DescribeServices                         │ AWS:${KVPipeline/Deploy/ECS-Deploy/CodePipel │                                               │
│   │                                              │        │ ecs:DescribeTaskDefinition                   │ ineActionRole}                               │                                               │
│   │                                              │        │ ecs:DescribeTasks                            │                                              │                                               │
│   │                                              │        │ ecs:ListTasks                                │                                              │                                               │
│   │                                              │        │ ecs:RegisterTaskDefinition                   │                                              │                                               │
│   │                                              │        │ ecs:UpdateService                            │                                              │                                               │
│ + │ *                                            │ Allow  │ iam:PassRole                                 │ AWS:${KVPipeline/Deploy/ECS-Deploy/CodePipel │ "StringEqualsIfExists": {                     │
│   │                                              │        │                                              │ ineActionRole}                               │   "iam:PassedToService": [                    │
│   │                                              │        │                                              │                                              │     "ec2.amazonaws.com",                      │
│   │                                              │        │                                              │                                              │     "ecs-tasks.amazonaws.com"                 │
│   │                                              │        │                                              │                                              │   ]                                           │
│   │                                              │        │                                              │                                              │ }                                             │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ arn:${AWS::Partition}:codebuild:us-east-1:71 │ Allow  │ codebuild:BatchPutCodeCoverages              │ AWS:${KVStore-build/Role}                    │                                               │
│   │ 4289824363:report-group/${KVStorebuild2B972C │        │ codebuild:BatchPutTestCases                  │                                              │                                               │
│   │ 73}-*                                        │        │ codebuild:CreateReport                       │                                              │                                               │
│   │                                              │        │ codebuild:CreateReportGroup                  │                                              │                                               │
│   │                                              │        │ codebuild:UpdateReport                       │                                              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ arn:${AWS::Partition}:ec2:${AWS::Region}:${A │ Allow  │ ec2:CreateNetworkInterfacePermission         │ AWS:${KVStore-build/Role}                    │ "StringEquals": {                             │
│   │ WS::AccountId}:network-interface/*           │        │                                              │                                              │   "ec2:Subnet": [                             │
│   │                                              │        │                                              │                                              │     "arn:${AWS::Partition}:ec2:${AWS::Region} │
│   │                                              │        │                                              │                                              │ :${AWS::AccountId}:subnet/${KvVpcPrivateSubne │
│   │                                              │        │                                              │                                              │ t1SubnetE2A4547A}",                           │
│   │                                              │        │                                              │                                              │     "arn:${AWS::Partition}:ec2:${AWS::Region} │
│   │                                              │        │                                              │                                              │ :${AWS::AccountId}:subnet/${KvVpcPrivateSubne │
│   │                                              │        │                                              │                                              │ t2SubnetC3540351}",                           │
│   │                                              │        │                                              │                                              │     "arn:${AWS::Partition}:ec2:${AWS::Region} │
│   │                                              │        │                                              │                                              │ :${AWS::AccountId}:subnet/${KvVpcPrivateSubne │
│   │                                              │        │                                              │                                              │ t3Subnet5B0F689B}"                            │
│   │                                              │        │                                              │                                              │   ],                                          │
│   │                                              │        │                                              │                                              │   "ec2:AuthorizedService": "codebuild.amazona │
│   │                                              │        │                                              │                                              │ ws.com"                                       │
│   │                                              │        │                                              │                                              │ }                                             │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ arn:${AWS::Partition}:logs:us-east-1:7142898 │ Allow  │ logs:CreateLogGroup                          │ AWS:${KVStore-build/Role}                    │                                               │
│   │ 24363:log-group:/aws/codebuild/${KVStorebuil │        │ logs:CreateLogStream                         │                                              │                                               │
│   │ d2B972C73}                                   │        │ logs:PutLogEvents                            │                                              │                                               │
│   │ arn:${AWS::Partition}:logs:us-east-1:7142898 │        │                                              │                                              │                                               │
│   │ 24363:log-group:/aws/codebuild/${KVStorebuil │        │                                              │                                              │                                               │
│   │ d2B972C73}:*                                 │        │                                              │                                              │                                               │
└───┴──────────────────────────────────────────────┴────────┴──────────────────────────────────────────────┴──────────────────────────────────────────────┴───────────────────────────────────────────────┘
IAM Policy Changes
┌───┬───────────────────────┬───────────────────────────────────────────────────────────────────────────┐
│   │ Resource              │ Managed Policy ARN                                                        │
├───┼───────────────────────┼───────────────────────────────────────────────────────────────────────────┤
│ + │ ${KVStore-build/Role} │ arn:${AWS::Partition}:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser │
└───┴───────────────────────┴───────────────────────────────────────────────────────────────────────────┘
Security Group Changes
┌───┬──────────────────────────────────────────────────────┬─────┬────────────┬──────────────────────────────────────────────────────┐
│   │ Group                                                │ Dir │ Protocol   │ Peer                                                 │
├───┼──────────────────────────────────────────────────────┼─────┼────────────┼──────────────────────────────────────────────────────┤
│ + │ ${KVStore-build/SecurityGroup.GroupId}               │ Out │ Everything │ Everyone (IPv4)                                      │
├───┼──────────────────────────────────────────────────────┼─────┼────────────┼──────────────────────────────────────────────────────┤
│ + │ ${KVappFargateService/LB/SecurityGroup.GroupId}      │ In  │ TCP 80     │ Everyone (IPv4)                                      │
│ + │ ${KVappFargateService/LB/SecurityGroup.GroupId}      │ Out │ TCP 80     │ ${KVappFargateService/Service/SecurityGroup.GroupId} │
├───┼──────────────────────────────────────────────────────┼─────┼────────────┼──────────────────────────────────────────────────────┤
│ + │ ${KVappFargateService/Service/SecurityGroup.GroupId} │ In  │ TCP 80     │ ${KVappFargateService/LB/SecurityGroup.GroupId}      │
│ + │ ${KVappFargateService/Service/SecurityGroup.GroupId} │ Out │ Everything │ Everyone (IPv4)                                      │
└───┴──────────────────────────────────────────────────────┴─────┴────────────┴──────────────────────────────────────────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)

Parameters
[+] Parameter BootstrapVersion BootstrapVersion: {"Type":"AWS::SSM::Parameter::Value<String>","Default":"/cdk-bootstrap/hnb659fds/version","Description":"Version of the CDK Bootstrap resources in this environment, automatically retrieved from SSM Parameter Store."}

Resources
[+] AWS::ECR::Repository kv-repo kvrepo78AD823A 
[+] AWS::EC2::VPC KvVpc KvVpc38150106 
[+] AWS::EC2::Subnet KvVpc/PublicSubnet1/Subnet KvVpcPublicSubnet1SubnetA9B5A0F9 
[+] AWS::EC2::RouteTable KvVpc/PublicSubnet1/RouteTable KvVpcPublicSubnet1RouteTableD496E32E 
[+] AWS::EC2::SubnetRouteTableAssociation KvVpc/PublicSubnet1/RouteTableAssociation KvVpcPublicSubnet1RouteTableAssociation956D43CD 
[+] AWS::EC2::Route KvVpc/PublicSubnet1/DefaultRoute KvVpcPublicSubnet1DefaultRoute4FA6A91D 
[+] AWS::EC2::EIP KvVpc/PublicSubnet1/EIP KvVpcPublicSubnet1EIP672F0BEF 
[+] AWS::EC2::NatGateway KvVpc/PublicSubnet1/NATGateway KvVpcPublicSubnet1NATGateway462BD0F1 
[+] AWS::EC2::Subnet KvVpc/PublicSubnet2/Subnet KvVpcPublicSubnet2Subnet31C4EC11 
[+] AWS::EC2::RouteTable KvVpc/PublicSubnet2/RouteTable KvVpcPublicSubnet2RouteTable70E1BCB9 
[+] AWS::EC2::SubnetRouteTableAssociation KvVpc/PublicSubnet2/RouteTableAssociation KvVpcPublicSubnet2RouteTableAssociationEE7E8671 
[+] AWS::EC2::Route KvVpc/PublicSubnet2/DefaultRoute KvVpcPublicSubnet2DefaultRoute64F32F53 
[+] AWS::EC2::EIP KvVpc/PublicSubnet2/EIP KvVpcPublicSubnet2EIP97727B4F 
[+] AWS::EC2::NatGateway KvVpc/PublicSubnet2/NATGateway KvVpcPublicSubnet2NATGatewayE3495D09 
[+] AWS::EC2::Subnet KvVpc/PublicSubnet3/Subnet KvVpcPublicSubnet3Subnet7025C82E 
[+] AWS::EC2::RouteTable KvVpc/PublicSubnet3/RouteTable KvVpcPublicSubnet3RouteTableE1288CA0 
[+] AWS::EC2::SubnetRouteTableAssociation KvVpc/PublicSubnet3/RouteTableAssociation KvVpcPublicSubnet3RouteTableAssociation5CC178F4 
[+] AWS::EC2::Route KvVpc/PublicSubnet3/DefaultRoute KvVpcPublicSubnet3DefaultRoute1409DB6F 
[+] AWS::EC2::EIP KvVpc/PublicSubnet3/EIP KvVpcPublicSubnet3EIPA724CB8A 
[+] AWS::EC2::NatGateway KvVpc/PublicSubnet3/NATGateway KvVpcPublicSubnet3NATGateway309288DA 
[+] AWS::EC2::Subnet KvVpc/PrivateSubnet1/Subnet KvVpcPrivateSubnet1SubnetE2A4547A 
[+] AWS::EC2::RouteTable KvVpc/PrivateSubnet1/RouteTable KvVpcPrivateSubnet1RouteTableE76E9EF5 
[+] AWS::EC2::SubnetRouteTableAssociation KvVpc/PrivateSubnet1/RouteTableAssociation KvVpcPrivateSubnet1RouteTableAssociation43E7FD9F 
[+] AWS::EC2::Route KvVpc/PrivateSubnet1/DefaultRoute KvVpcPrivateSubnet1DefaultRoute79E51971 
[+] AWS::EC2::Subnet KvVpc/PrivateSubnet2/Subnet KvVpcPrivateSubnet2SubnetC3540351 
[+] AWS::EC2::RouteTable KvVpc/PrivateSubnet2/RouteTable KvVpcPrivateSubnet2RouteTable273EFFF7 
[+] AWS::EC2::SubnetRouteTableAssociation KvVpc/PrivateSubnet2/RouteTableAssociation KvVpcPrivateSubnet2RouteTableAssociationE92B2179 
[+] AWS::EC2::Route KvVpc/PrivateSubnet2/DefaultRoute KvVpcPrivateSubnet2DefaultRouteF93E6706 
[+] AWS::EC2::Subnet KvVpc/PrivateSubnet3/Subnet KvVpcPrivateSubnet3Subnet5B0F689B 
[+] AWS::EC2::RouteTable KvVpc/PrivateSubnet3/RouteTable KvVpcPrivateSubnet3RouteTableEEFA0146 
[+] AWS::EC2::SubnetRouteTableAssociation KvVpc/PrivateSubnet3/RouteTableAssociation KvVpcPrivateSubnet3RouteTableAssociation84F9D8CF 
[+] AWS::EC2::Route KvVpc/PrivateSubnet3/DefaultRoute KvVpcPrivateSubnet3DefaultRouteB18AACFB 
[+] AWS::EC2::InternetGateway KvVpc/IGW KvVpcIGW4A328FB4 
[+] AWS::EC2::VPCGatewayAttachment KvVpc/VPCGW KvVpcVPCGW7F4C2A06 
[+] AWS::ECS::Cluster KvEcsCluster KvEcsCluster9799C487 
[+] AWS::ElasticLoadBalancingV2::LoadBalancer KVappFargateService/LB KVappFargateServiceLBAE7622C1 
[+] AWS::EC2::SecurityGroup KVappFargateService/LB/SecurityGroup KVappFargateServiceLBSecurityGroup8F126FED 
[+] AWS::EC2::SecurityGroupEgress KVappFargateService/LB/SecurityGroup/to CdkKvStackKVappFargateServiceSecurityGroupB618D5E7:80 KVappFargateServiceLBSecurityGrouptoCdkKvStackKVappFargateServiceSecurityGroupB618D5E78093709048 
[+] AWS::ElasticLoadBalancingV2::Listener KVappFargateService/LB/PublicListener KVappFargateServiceLBPublicListener1D60906C 
[+] AWS::ElasticLoadBalancingV2::TargetGroup KVappFargateService/LB/PublicListener/ECSGroup KVappFargateServiceLBPublicListenerECSGroup34AACB42 
[+] AWS::IAM::Role KVappFargateService/TaskDef/TaskRole KVappFargateServiceTaskDefTaskRole29C425A4 
[+] AWS::ECS::TaskDefinition KVappFargateService/TaskDef KVappFargateServiceTaskDefCA0C18FE 
[+] AWS::Logs::LogGroup KVappFargateService/TaskDef/web/LogGroup KVappFargateServiceTaskDefwebLogGroup55AEB72E 
[+] AWS::IAM::Role KVappFargateService/TaskDef/ExecutionRole KVappFargateServiceTaskDefExecutionRole1B5C61AE 
[+] AWS::IAM::Policy KVappFargateService/TaskDef/ExecutionRole/DefaultPolicy KVappFargateServiceTaskDefExecutionRoleDefaultPolicyBC91778E 
[+] AWS::ECS::Service KVappFargateService/Service/Service KVappFargateService64EDA79E 
[+] AWS::EC2::SecurityGroup KVappFargateService/Service/SecurityGroup KVappFargateServiceSecurityGroup72DD2C6E 
[+] AWS::EC2::SecurityGroupIngress KVappFargateService/Service/SecurityGroup/from CdkKvStackKVappFargateServiceLBSecurityGroupAD8C61F7:80 KVappFargateServiceSecurityGroupfromCdkKvStackKVappFargateServiceLBSecurityGroupAD8C61F780F88976E4 
[+] AWS::IAM::Role KVStore-build/Role KVStorebuildRole8D7C1AB4 
[+] AWS::IAM::Policy KVStore-build/Role/DefaultPolicy KVStorebuildRoleDefaultPolicy06261DE7 
[+] AWS::EC2::SecurityGroup KVStore-build/SecurityGroup KVStorebuildSecurityGroup8FDD6F2B 
[+] AWS::CodeBuild::Project KVStore-build KVStorebuild2B972C73 
[+] AWS::IAM::Policy KVStore-build/PolicyDocument KVStorebuildPolicyDocumentC6315A2A 
[+] AWS::KMS::Key KVPipeline/ArtifactsBucketEncryptionKey KVPipelineArtifactsBucketEncryptionKeyC2A8BD95 
[+] AWS::KMS::Alias KVPipeline/ArtifactsBucketEncryptionKeyAlias KVPipelineArtifactsBucketEncryptionKeyAlias9D389EFA 
[+] AWS::S3::Bucket KVPipeline/ArtifactsBucket KVPipelineArtifactsBucket517A6764 
[+] AWS::IAM::Role KVPipeline/Role KVPipelineRoleA3859E5C 
[+] AWS::IAM::Policy KVPipeline/Role/DefaultPolicy KVPipelineRoleDefaultPolicyA651A01F 
[+] AWS::CodePipeline::Pipeline KVPipeline KVPipeline7C019401 
[+] AWS::IAM::Role KVPipeline/Build/TestBuild-action/CodePipelineActionRole KVPipelineBuildTestBuildactionCodePipelineActionRoleEDE57B12 
[+] AWS::IAM::Policy KVPipeline/Build/TestBuild-action/CodePipelineActionRole/DefaultPolicy KVPipelineBuildTestBuildactionCodePipelineActionRoleDefaultPolicy33EA8093 
[+] AWS::IAM::Role KVPipeline/Deploy/ECS-Deploy/CodePipelineActionRole KVPipelineDeployECSDeployCodePipelineActionRole81CF2309 
[+] AWS::IAM::Policy KVPipeline/Deploy/ECS-Deploy/CodePipelineActionRole/DefaultPolicy KVPipelineDeployECSDeployCodePipelineActionRoleDefaultPolicyFA1FC834 

Outputs
[+] Output KVappFargateService/LoadBalancerDNS KVappFargateServiceLoadBalancerDNS4524CDFE: {"Value":{"Fn::GetAtt":["KVappFargateServiceLBAE7622C1","DNSName"]}}
[+] Output KVappFargateService/ServiceURL KVappFargateServiceServiceURLDE2C1996: {"Value":{"Fn::Join":["",["http://",{"Fn::GetAtt":["KVappFargateServiceLBAE7622C1","DNSName"]}]]}}

Other Changes
[+] Unknown Rules: {"CheckBootstrapVersion":{"Assertions":[{"Assert":{"Fn::Not":[{"Fn::Contains":[["1","2","3","4","5"],{"Ref":"BootstrapVersion"}]}]},"AssertDescription":"CDK bootstrap stack version 6 required. Please run 'cdk bootstrap' with a recent version of the CDK CLI."}]}}
```
Deploy the stack

```
$ cdk deploy                                               
This deployment will make potentially sensitive changes according to your current security approval level (--require-approval broadening).
Please confirm you intend to make the following modifications:

IAM Statement Changes
┌───┬──────────────────────────────────────────────┬────────┬──────────────────────────────────────────────┬──────────────────────────────────────────────┬───────────────────────────────────────────────┐
│   │ Resource                                     │ Effect │ Action                                       │ Principal                                    │ Condition                                     │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVPipeline/ArtifactsBucket.Arn}            │ Allow  │ s3:Abort*                                    │ AWS:${KVStore-build/Role}                    │                                               │
│   │ ${KVPipeline/ArtifactsBucket.Arn}/*          │        │ s3:DeleteObject*                             │                                              │                                               │
│   │                                              │        │ s3:GetBucket*                                │                                              │                                               │
│   │                                              │        │ s3:GetObject*                                │                                              │                                               │
│   │                                              │        │ s3:List*                                     │                                              │                                               │
│   │                                              │        │ s3:PutObject                                 │                                              │                                               │
│ + │ ${KVPipeline/ArtifactsBucket.Arn}            │ Allow  │ s3:Abort*                                    │ AWS:${KVPipeline/Role}                       │                                               │
│   │ ${KVPipeline/ArtifactsBucket.Arn}/*          │        │ s3:DeleteObject*                             │                                              │                                               │
│   │                                              │        │ s3:GetBucket*                                │                                              │                                               │
│   │                                              │        │ s3:GetObject*                                │                                              │                                               │
│   │                                              │        │ s3:List*                                     │                                              │                                               │
│   │                                              │        │ s3:PutObject                                 │                                              │                                               │
│ + │ ${KVPipeline/ArtifactsBucket.Arn}            │ Allow  │ s3:GetBucket*                                │ AWS:${KVPipeline/Deploy/ECS-Deploy/CodePipel │                                               │
│   │ ${KVPipeline/ArtifactsBucket.Arn}/*          │        │ s3:GetObject*                                │ ineActionRole}                               │                                               │
│   │                                              │        │ s3:List*                                     │                                              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVPipeline/ArtifactsBucketEncryptionKey.Ar │ Allow  │ kms:*                                        │ AWS:arn:${AWS::Partition}:iam::714289824363: │                                               │
│   │ n}                                           │        │                                              │ root                                         │                                               │
│ + │ ${KVPipeline/ArtifactsBucketEncryptionKey.Ar │ Allow  │ kms:Decrypt                                  │ AWS:${KVStore-build/Role}                    │                                               │
│   │ n}                                           │        │ kms:DescribeKey                              │                                              │                                               │
│   │                                              │        │ kms:Encrypt                                  │                                              │                                               │
│   │                                              │        │ kms:GenerateDataKey*                         │                                              │                                               │
│   │                                              │        │ kms:ReEncrypt*                               │                                              │                                               │
│ + │ ${KVPipeline/ArtifactsBucketEncryptionKey.Ar │ Allow  │ kms:Decrypt                                  │ AWS:${KVStore-build/Role}                    │                                               │
│   │ n}                                           │        │ kms:Encrypt                                  │                                              │                                               │
│   │                                              │        │ kms:GenerateDataKey*                         │                                              │                                               │
│   │                                              │        │ kms:ReEncrypt*                               │                                              │                                               │
│ + │ ${KVPipeline/ArtifactsBucketEncryptionKey.Ar │ Allow  │ kms:Decrypt                                  │ AWS:${KVPipeline/Role}                       │                                               │
│   │ n}                                           │        │ kms:DescribeKey                              │                                              │                                               │
│   │                                              │        │ kms:Encrypt                                  │                                              │                                               │
│   │                                              │        │ kms:GenerateDataKey*                         │                                              │                                               │
│   │                                              │        │ kms:ReEncrypt*                               │                                              │                                               │
│ + │ ${KVPipeline/ArtifactsBucketEncryptionKey.Ar │ Allow  │ kms:Decrypt                                  │ AWS:${KVPipeline/Deploy/ECS-Deploy/CodePipel │                                               │
│   │ n}                                           │        │ kms:DescribeKey                              │ ineActionRole}                               │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVPipeline/Build/TestBuild-action/CodePipe │ Allow  │ sts:AssumeRole                               │ AWS:arn:${AWS::Partition}:iam::714289824363: │                                               │
│   │ lineActionRole.Arn}                          │        │                                              │ root                                         │                                               │
│ + │ ${KVPipeline/Build/TestBuild-action/CodePipe │ Allow  │ sts:AssumeRole                               │ AWS:${KVPipeline/Role}                       │                                               │
│   │ lineActionRole.Arn}                          │        │                                              │                                              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVPipeline/Deploy/ECS-Deploy/CodePipelineA │ Allow  │ sts:AssumeRole                               │ AWS:arn:${AWS::Partition}:iam::714289824363: │                                               │
│   │ ctionRole.Arn}                               │        │                                              │ root                                         │                                               │
│ + │ ${KVPipeline/Deploy/ECS-Deploy/CodePipelineA │ Allow  │ sts:AssumeRole                               │ AWS:${KVPipeline/Role}                       │                                               │
│   │ ctionRole.Arn}                               │        │                                              │                                              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVPipeline/Role.Arn}                       │ Allow  │ sts:AssumeRole                               │ Service:codepipeline.amazonaws.com           │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVStore-build.Arn}                         │ Allow  │ codebuild:BatchGetBuilds                     │ AWS:${KVPipeline/Build/TestBuild-action/Code │                                               │
│   │                                              │        │ codebuild:StartBuild                         │ PipelineActionRole}                          │                                               │
│   │                                              │        │ codebuild:StopBuild                          │                                              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVStore-build/Role.Arn}                    │ Allow  │ sts:AssumeRole                               │ Service:codebuild.amazonaws.com              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVappFargateService/TaskDef/ExecutionRole. │ Allow  │ sts:AssumeRole                               │ Service:ecs-tasks.amazonaws.com              │                                               │
│   │ Arn}                                         │        │                                              │                                              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVappFargateService/TaskDef/TaskRole.Arn}  │ Allow  │ sts:AssumeRole                               │ Service:ecs-tasks.amazonaws.com              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${KVappFargateService/TaskDef/web/LogGroup.A │ Allow  │ logs:CreateLogStream                         │ AWS:${KVappFargateService/TaskDef/ExecutionR │                                               │
│   │ rn}                                          │        │ logs:PutLogEvents                            │ ole}                                         │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ ${kv-repo.Arn}                               │ Allow  │ ecr:BatchCheckLayerAvailability              │ AWS:${KVappFargateService/TaskDef/ExecutionR │                                               │
│   │                                              │        │ ecr:BatchGetImage                            │ ole}                                         │                                               │
│   │                                              │        │ ecr:GetDownloadUrlForLayer                   │                                              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ *                                            │ Allow  │ ecr:GetAuthorizationToken                    │ AWS:${KVappFargateService/TaskDef/ExecutionR │                                               │
│   │                                              │        │                                              │ ole}                                         │                                               │
│ + │ *                                            │ Allow  │ ec2:CreateNetworkInterface                   │ AWS:${KVStore-build/Role}                    │                                               │
│   │                                              │        │ ec2:DeleteNetworkInterface                   │                                              │                                               │
│   │                                              │        │ ec2:DescribeDhcpOptions                      │                                              │                                               │
│   │                                              │        │ ec2:DescribeNetworkInterfaces                │                                              │                                               │
│   │                                              │        │ ec2:DescribeSecurityGroups                   │                                              │                                               │
│   │                                              │        │ ec2:DescribeSubnets                          │                                              │                                               │
│   │                                              │        │ ec2:DescribeVpcs                             │                                              │                                               │
│ + │ *                                            │ Allow  │ ecs:DescribeServices                         │ AWS:${KVPipeline/Deploy/ECS-Deploy/CodePipel │                                               │
│   │                                              │        │ ecs:DescribeTaskDefinition                   │ ineActionRole}                               │                                               │
│   │                                              │        │ ecs:DescribeTasks                            │                                              │                                               │
│   │                                              │        │ ecs:ListTasks                                │                                              │                                               │
│   │                                              │        │ ecs:RegisterTaskDefinition                   │                                              │                                               │
│   │                                              │        │ ecs:UpdateService                            │                                              │                                               │
│ + │ *                                            │ Allow  │ iam:PassRole                                 │ AWS:${KVPipeline/Deploy/ECS-Deploy/CodePipel │ "StringEqualsIfExists": {                     │
│   │                                              │        │                                              │ ineActionRole}                               │   "iam:PassedToService": [                    │
│   │                                              │        │                                              │                                              │     "ec2.amazonaws.com",                      │
│   │                                              │        │                                              │                                              │     "ecs-tasks.amazonaws.com"                 │
│   │                                              │        │                                              │                                              │   ]                                           │
│   │                                              │        │                                              │                                              │ }                                             │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ arn:${AWS::Partition}:codebuild:us-east-1:71 │ Allow  │ codebuild:BatchPutCodeCoverages              │ AWS:${KVStore-build/Role}                    │                                               │
│   │ 4289824363:report-group/${KVStorebuild2B972C │        │ codebuild:BatchPutTestCases                  │                                              │                                               │
│   │ 73}-*                                        │        │ codebuild:CreateReport                       │                                              │                                               │
│   │                                              │        │ codebuild:CreateReportGroup                  │                                              │                                               │
│   │                                              │        │ codebuild:UpdateReport                       │                                              │                                               │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ arn:${AWS::Partition}:ec2:${AWS::Region}:${A │ Allow  │ ec2:CreateNetworkInterfacePermission         │ AWS:${KVStore-build/Role}                    │ "StringEquals": {                             │
│   │ WS::AccountId}:network-interface/*           │        │                                              │                                              │   "ec2:Subnet": [                             │
│   │                                              │        │                                              │                                              │     "arn:${AWS::Partition}:ec2:${AWS::Region} │
│   │                                              │        │                                              │                                              │ :${AWS::AccountId}:subnet/${KvVpcPrivateSubne │
│   │                                              │        │                                              │                                              │ t1SubnetE2A4547A}",                           │
│   │                                              │        │                                              │                                              │     "arn:${AWS::Partition}:ec2:${AWS::Region} │
│   │                                              │        │                                              │                                              │ :${AWS::AccountId}:subnet/${KvVpcPrivateSubne │
│   │                                              │        │                                              │                                              │ t2SubnetC3540351}",                           │
│   │                                              │        │                                              │                                              │     "arn:${AWS::Partition}:ec2:${AWS::Region} │
│   │                                              │        │                                              │                                              │ :${AWS::AccountId}:subnet/${KvVpcPrivateSubne │
│   │                                              │        │                                              │                                              │ t3Subnet5B0F689B}"                            │
│   │                                              │        │                                              │                                              │   ],                                          │
│   │                                              │        │                                              │                                              │   "ec2:AuthorizedService": "codebuild.amazona │
│   │                                              │        │                                              │                                              │ ws.com"                                       │
│   │                                              │        │                                              │                                              │ }                                             │
├───┼──────────────────────────────────────────────┼────────┼──────────────────────────────────────────────┼──────────────────────────────────────────────┼───────────────────────────────────────────────┤
│ + │ arn:${AWS::Partition}:logs:us-east-1:7142898 │ Allow  │ logs:CreateLogGroup                          │ AWS:${KVStore-build/Role}                    │                                               │
│   │ 24363:log-group:/aws/codebuild/${KVStorebuil │        │ logs:CreateLogStream                         │                                              │                                               │
│   │ d2B972C73}                                   │        │ logs:PutLogEvents                            │                                              │                                               │
│   │ arn:${AWS::Partition}:logs:us-east-1:7142898 │        │                                              │                                              │                                               │
│   │ 24363:log-group:/aws/codebuild/${KVStorebuil │        │                                              │                                              │                                               │
│   │ d2B972C73}:*                                 │        │                                              │                                              │                                               │
└───┴──────────────────────────────────────────────┴────────┴──────────────────────────────────────────────┴──────────────────────────────────────────────┴───────────────────────────────────────────────┘
IAM Policy Changes
┌───┬───────────────────────┬───────────────────────────────────────────────────────────────────────────┐
│   │ Resource              │ Managed Policy ARN                                                        │
├───┼───────────────────────┼───────────────────────────────────────────────────────────────────────────┤
│ + │ ${KVStore-build/Role} │ arn:${AWS::Partition}:iam::aws:policy/AmazonEC2ContainerRegistryPowerUser │
└───┴───────────────────────┴───────────────────────────────────────────────────────────────────────────┘
Security Group Changes
┌───┬──────────────────────────────────────────────────────┬─────┬────────────┬──────────────────────────────────────────────────────┐
│   │ Group                                                │ Dir │ Protocol   │ Peer                                                 │
├───┼──────────────────────────────────────────────────────┼─────┼────────────┼──────────────────────────────────────────────────────┤
│ + │ ${KVStore-build/SecurityGroup.GroupId}               │ Out │ Everything │ Everyone (IPv4)                                      │
├───┼──────────────────────────────────────────────────────┼─────┼────────────┼──────────────────────────────────────────────────────┤
│ + │ ${KVappFargateService/LB/SecurityGroup.GroupId}      │ In  │ TCP 80     │ Everyone (IPv4)                                      │
│ + │ ${KVappFargateService/LB/SecurityGroup.GroupId}      │ Out │ TCP 80     │ ${KVappFargateService/Service/SecurityGroup.GroupId} │
├───┼──────────────────────────────────────────────────────┼─────┼────────────┼──────────────────────────────────────────────────────┤
│ + │ ${KVappFargateService/Service/SecurityGroup.GroupId} │ In  │ TCP 80     │ ${KVappFargateService/LB/SecurityGroup.GroupId}      │
│ + │ ${KVappFargateService/Service/SecurityGroup.GroupId} │ Out │ Everything │ Everyone (IPv4)                                      │
└───┴──────────────────────────────────────────────────────┴─────┴────────────┴──────────────────────────────────────────────────────┘
(NOTE: There may be security-related changes not in this list. See https://github.com/aws/aws-cdk/issues/1299)

Do you wish to deploy these changes (y/n)? y
CdkKvStack: deploying...
[0%] start: Publishing 73f265908516c80dd92b96971b359c30775116ce7703b4da06b60a7abb80d010:714289824363-us-east-1
[100%] success: Published 73f265908516c80dd92b96971b359c30775116ce7703b4da06b60a7abb80d010:714289824363-us-east-1
CdkKvStack: creating CloudFormation changeset...

 ✅  CdkKvStack

Outputs:
CdkKvStack.KVappFargateServiceLoadBalancerDNS4524CDFE = CdkKv-KVapp-11NICSPCPNPQH-323369672.us-east-1.elb.amazonaws.com
CdkKvStack.KVappFargateServiceServiceURLDE2C1996 = http://CdkKv-KVapp-11NICSPCPNPQH-323369672.us-east-1.elb.amazonaws.com

Stack ARN:
arn:aws:cloudformation:us-east-1:714289824363:stack/CdkKvStack/f501fbf0-f449-11eb-92c0-0e3caa6b31bf
```
Destroy the resources

```
$ cdk destroy
Are you sure you want to delete: CdkKvStack (y/n)? y
CdkKvStack: destroying...

 ✅  CdkKvStack: destroyed
```
To add additional dependencies, for example other CDK libraries, just add
them to your `setup.py` file and rerun the `pip install -r requirements.txt`
command.

## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

Enjoy!
