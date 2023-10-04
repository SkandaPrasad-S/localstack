# LocalStack Resource Provider Scaffolding v2
from __future__ import annotations

from pathlib import Path
from typing import Optional, Type, TypedDict

import localstack.services.cloudformation.provider_utils as util
from localstack.services.cloudformation.resource_provider import (
    CloudFormationResourceProviderPlugin,
    OperationStatus,
    ProgressEvent,
    ResourceProvider,
    ResourceRequest,
)


class EC2RouteProperties(TypedDict):
    RouteTableId: Optional[str]
    CarrierGatewayId: Optional[str]
    DestinationCidrBlock: Optional[str]
    DestinationIpv6CidrBlock: Optional[str]
    EgressOnlyInternetGatewayId: Optional[str]
    GatewayId: Optional[str]
    Id: Optional[str]
    InstanceId: Optional[str]
    LocalGatewayId: Optional[str]
    NatGatewayId: Optional[str]
    NetworkInterfaceId: Optional[str]
    TransitGatewayId: Optional[str]
    VpcEndpointId: Optional[str]
    VpcPeeringConnectionId: Optional[str]


REPEATED_INVOCATION = "repeated_invocation"


class EC2RouteProvider(ResourceProvider[EC2RouteProperties]):

    TYPE = "AWS::EC2::Route"  # Autogenerated. Don't change
    SCHEMA = util.get_schema_path(Path(__file__))  # Autogenerated. Don't change

    def create(
        self,
        request: ResourceRequest[EC2RouteProperties],
    ) -> ProgressEvent[EC2RouteProperties]:
        """
        Create a new resource.

        Primary identifier fields:
          - /properties/Id

        Required properties:
          - RouteTableId

        Create-only properties:
          - /properties/RouteTableId
          - /properties/DestinationCidrBlock

        Read-only properties:
          - /properties/Id



        """
        model = request.desired_state
        ec2 = request.aws_client_factory.ec2

        cidr_block = model.get("DestinationCidrBlock")
        ipv6_cidr_block = model.get("DestinationIpv6CidrBlock", "")

        ec2.create_route(
            DestinationCidrBlock=cidr_block,
            DestinationIpv6CidrBlock=ipv6_cidr_block,
            RouteTableId=model["RouteTableId"],
        )

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def read(
        self,
        request: ResourceRequest[EC2RouteProperties],
    ) -> ProgressEvent[EC2RouteProperties]:
        """
        Fetch resource information


        """
        raise NotImplementedError

    def delete(
        self,
        request: ResourceRequest[EC2RouteProperties],
    ) -> ProgressEvent[EC2RouteProperties]:
        """
        Delete a resource


        """
        model = request.desired_state
        ec2 = request.aws_client_factory.ec2

        cidr_block = model.get("DestinationCidrBlock")
        ipv6_cidr_block = model.get("DestinationIpv6CidrBlock", "")

        try:
            ec2.delete_route(
                DestinationCidrBlock=cidr_block,
                DestinationIpv6CidrBlock=ipv6_cidr_block,
                RouteTableId=model["RouteTableId"],
            )
        except ec2.exceptions.ClientError:
            pass

        return ProgressEvent(
            status=OperationStatus.SUCCESS,
            resource_model=model,
            custom_context=request.custom_context,
        )

    def update(
        self,
        request: ResourceRequest[EC2RouteProperties],
    ) -> ProgressEvent[EC2RouteProperties]:
        """
        Update a resource


        """
        raise NotImplementedError
