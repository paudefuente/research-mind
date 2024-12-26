"""
This module contains the command line interface for the application. Each command
is defined as a function that is called when the command is executed in the terminal,
enabling interactuate with the library in a more user-friendly way.

authors = [
    "@paudefuente",
]
"""


import click

from core import __version__


@click.command()
def welcome():
    """
    Welcome to ResMind, the Python Library for Research and Innovation
    """
    
    click.echo("""
        8888888b.  8888888888 .d8888b.  888b     d888 8888888 888b    888 8888888b.  
        888   Y88b 888       d88P  Y88b 8888b   d8888   888   8888b   888 888  "Y88b 
        888    888 888       Y88b.      88888b.d88888   888   88888b  888 888    888 
        888   d88P 8888888    "Y888b.   888Y88888P888   888   888Y88b 888 888    888 
        8888888P"  888           "Y88b. 888 Y888P 888   888   888 Y88b888 888    888 
        888 T88b   888             "888 888  Y8P  888   888   888  Y88888 888    888 
        888  T88b  888       Y88b  d88P 888   "   888   888   888   Y8888 888  .d88P 
        888   T88b 8888888888 "Y8888P"  888       888 8888888 888    Y888 8888888P"  
                                                                             
        🌟 Welcome to **ResMind** 🌟
        The Python Library for Research and Innovation.
    
        🚀 Empowering your knowledge journey
        with cutting-edge innovation and precision.

        ✨ Let's explore the future together! ✨
    """)

@click.command()
@click.argument('name')
def greet(name):
    """Greet the user by name"""
    click.echo(f'Hello, {name}!')




