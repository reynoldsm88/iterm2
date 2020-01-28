#!/usr/bin/env python3

import iterm2
import boto3

# To install, update, or remove packages from PyPI, use Scripts > Manage > Manage Dependencies...
def get_instance_name( instance: dict ):
    for tag in instance[ "Tags" ]:
        if tag[ "Key" ] == "Name":
            return tag[ "Value" ]

def get_ec2_instances( filters: list = [ ] ) -> list:
    aws_filters = []
    for filter in filters:
        tag_name, tag_value = filter
        aws_filters.append( { "Name": f"tag:{tag_name}", "Values": tag_value } )
    ec2_instances = [ ]
    client = boto3.client( "ec2" )
    response = client.describe_instances( Filters = aws_filters )
    for reservation in response[ "Reservations" ]:
        for instance in reservation[ "Instances" ]:
            pub_dns = instance[ "PublicDnsName" ]
            name = get_instance_name( instance )
            ec2_instances.append( (name, pub_dns) )
    return sorted( ec2_instances )


def trim_prefix( name: str ):
    return name.split( "michael-dart-" )[ -1 ]

async def main( connection ):
    tag_filters = [ ("Name", [ "michael-dart*" ]), 
                    ("dart.role", [ "data-master", "data-worker", "batch-master", "batch-worker" ] ) ]

    app = await iterm2.async_get_app( connection )
    window = app.current_terminal_window
    if window is not None:
        for instance in get_ec2_instances( tag_filters ):
            name, dns = instance
            tab_name = trim_prefix( name )
            cmd = f"ssh centos@{dns}"
            tab = await window.async_create_tab( command = cmd )
            await tab.async_set_title( tab_name )
    else:
        # You can view this message in the script console.
        print( "There is no current session window to open in" )


iterm2.run_until_complete( main )#!/usr/bin/env python3

import iterm2
import boto3

# To install, update, or remove packages from PyPI, use Scripts > Manage > Manage Dependencies...
def get_instance_name( instance: dict ):
    for tag in instance[ "Tags" ]:
        if tag[ "Key" ] == "Name":
            return tag[ "Value" ]

def get_ec2_instances( filters: list = [ ] ) -> list:
    aws_filters = []
    for filter in filters:
        tag_name, tag_value = filter
        aws_filters.append( { "Name": f"tag:{tag_name}", "Values": tag_value } )
    ec2_instances = [ ]
    client = boto3.client( "ec2" )
    response = client.describe_instances( Filters = aws_filters )
    for reservation in response[ "Reservations" ]:
        for instance in reservation[ "Instances" ]:
            pub_dns = instance[ "PublicDnsName" ]
            name = get_instance_name( instance )
            ec2_instances.append( (name, pub_dns) )
    return sorted( ec2_instances )


def trim_prefix( prefix: str  instance_name: str ):
    return name.split( prefix )[ -1 ]

async def main( connection ):
    name_prefix = "my-prefix-"
    tag_filters = [ ("Name", [ f"{name_prefix}*" ] ),
                    ("my.role", [ "foo", "bar" ] ) ]

    app = await iterm2.async_get_app( connection )
    window = app.current_terminal_window
    if window is not None:
        for instance in get_ec2_instances( tag_filters ):
            name, dns = instance
            tab_name = trim_prefix( name )
            cmd = f"ssh centos@{dns}"
            tab = await window.async_create_tab( command = cmd )
            await tab.async_set_title( tab_name )
    else:
        # You can view this message in the script console.
        print( "There is no current session window to open in" )


iterm2.run_until_complete( main )
