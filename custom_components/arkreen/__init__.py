from homeassistant.helpers import entity_registry
from homeassistant.helpers import device_registry

from homeassistant.helpers.device_registry import async_get as async_get_device_registry
from homeassistant.helpers.entity_registry import async_get as async_get_entity_registry

import logging
from homeassistant.core import callback
from homeassistant import config_entries
from homeassistant.helpers import config_entry_oauth2_flow
#from .config_flow import RpcConfigFlow

_LOGGER = logging.getLogger(__name__)

DOMAIN = "arkreen"

import asyncio
from datetime import timedelta
from homeassistant.core import callback, HomeAssistant
from homeassistant.helpers.event import async_call_later, async_track_time_interval

import aiohttp

from homeassistant.helpers.storage import Store
STORAGE_KEY = f"{DOMAIN}_config"
STORAGE_VERSION = 1

from functools import partial
from homeassistant.core import ServiceCall
import json

from homeassistant.components.http import HomeAssistantView
from aiohttp import web

class DevicesWithEntitiesView(HomeAssistantView):
    """View to handle devices with entities requests."""

    url = f"/api/{DOMAIN}/devices_with_entities"
    name = f"api:{DOMAIN}:devices_with_entities"

    async def get(self, request):
        """Handle GET request for devices with entities."""
        hass = request.app['hass']
        domain_data = hass.data.get(DOMAIN, {})
        devices_with_entities = domain_data.get('devices_with_entities', [])

        return web.json_response(devices_with_entities)
        
async def send_push_data(hass: HomeAssistant, plant_id: str, owner: str, power: str, energy: str):
    #url = "http://192.168.71.34:3000/hapush"
    url = "http://192.168.71.34:19812/asp/homeassistant/push"
    headers = {'Content-Type': 'application/json'}
    data = {
        "accumulated_yield_energy": energy, 
        "input_power": power,   
        "owner": owner,
        "plant_id": plant_id
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers={'Content-Type': 'application/json'}, json=data) as response:
                if response.status == 200:
                    _LOGGER.info("Data sent successfully.")
                    response_json = await response.text()
                    _LOGGER.info("Response from server: %s", response_json)
                else:
                    _LOGGER.error("Failed to send data. Status code: %d", response.status)
                    text = await response.text()
                    _LOGGER.error("Response body: %s", text)
    except aiohttp.ClientError as err:
        _LOGGER.error("Error sending data: %s", err)


# 定义要发送的数据结构
RPC_URL = "http://192.168.71.34:3000/rpc"  # 替换为实际的RPC接口URL
HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer YOUR_ACCESS_TOKEN',  # 如果需要认证，请替换为真实的访问令牌
}

async def send_rpc_data(hass: HomeAssistant, plant_id: str, owner: str, power: str, energy: str):
    """Send data to the external RPC interface using the provided token."""
    rpc_request_body = {
        "jsonrpc": "2.0",
        "method": "receiveData",
        "params": {
            "accumulated_yield_energy": energy,
            "input_power": power,
            "owner": owner,
            "plant_id": plant_id
        },
        "id": 1
    }

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(RPC_URL, headers={"Authorization": f"Bearer {plant_id}"}, json=rpc_request_body) as response:
                if response.status == 200:
                    _LOGGER.error("Data sent successfully.")
                    response_json = await response.json()
                    _LOGGER.debug("Response from server: %s", response_json)
                else:
                    _LOGGER.error("Failed to send data. Status code: %d", response.status)
                    text = await response.text()
                    _LOGGER.error("Response body: %s", text)
    except aiohttp.ClientError as err:
        _LOGGER.error("Error sending data: %s", err)

# 定义你想要定期执行的函数
async def my_periodic_function(hass: HomeAssistant, now=None):
    """定期执行的函数."""
    _LOGGER.debug("new arkreen Executing periodic function")
    # 在这里放置你的逻辑代码
    await arkreen_collect_and_log_device_info(hass)
    pass



async def async_setup(hass, config):
    """Set up the example integration."""  

    # 注册新的RESTful API端点
    hass.http.register_view(DevicesWithEntitiesView())    
     
    # Initialize storage
    
    store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
    #await store.async_save({});
    
    # Load existing data from storage or initialize with empty dict
    data = await store.async_load() or {}

    hass.data[DOMAIN] = {
        'store': store,
        'data': data
    }
    
    
    hass.states.async_set("arkreen.arkreen", "Arkreen")

    # Register the save_config service
    async def _handle_save_config_service(call):
        """Handle the service call."""
        # Extract parameters from the service call
        config = call.data

        device = call.data.get('device')
        plant_id = call.data.get('plant_id')
        owner = call.data.get('owner')

        if not device or not plant_id or not owner:
            _LOGGER.error(f"ark All fields are required", config)
            return

        hass.states.async_set("arkreen.arkreen", "Arkreen s")
    
        # Save new configuration to data
        hass.data[DOMAIN]['data'][device] = {
            'plant_id': plant_id,
            'owner': owner
        }

        # Write data back to storage
        await hass.data[DOMAIN]['store'].async_save(hass.data[DOMAIN]['data'])

        _LOGGER.info(f"Configuration for {device} saved.")

        _LOGGER.error("arkreen Configuration saved: %s", config)
    
    hass.services.async_register(DOMAIN, 'save_config', _handle_save_config_service)

    async def _handle_get_devices_with_entities_service(call: ServiceCall):
        
        result = await get_devices_with_entities(hass)
        #result = await hass.async_add_executor_job(get_devices_with_entities, hass)
        print(f"  result: {result}")
        # 将结果存储在HASS的数据字典中，以便可以在其他地方访问它
        #hass.states.setdefault(DOMAIN, {})['devices_with_entities'] = result
        #hass.states.async_set("arkreen.devices_with_entities", result)
        hass.data.setdefault(DOMAIN, {})['devices_with_entities'] = result
        return result
        
    hass.services.async_register(DOMAIN, 'get_devices_with_entities', _handle_get_devices_with_entities_service)
   
    # 创建一个时间间隔调度器，例如每1分钟执行一次
    interval = timedelta(seconds = 60)
    
    #@callback
    #def schedule_periodic_task(now):
        #"""Schedule the periodic task."""
 
        #hass.async_create_task(my_periodic_function(hass, now))
    # 立即安排第一次执行，并设置后续的周期性执行
    #hass.async_create_task(arkreen_collect_and_log_device_info(hass))  # 立即执行一次
    #async_track_time_interval(hass, schedule_periodic_task, interval)  
    @callback
    def schedule_periodic_task(now):
        """Schedule the periodic task."""
        hass.async_create_task(my_periodic_function(hass, now))

    # Define a one-time task that will be executed after a 10-second delay
    async def initial_delay_callback(event_time):
        # Execute the task you want to run immediately once
        hass.async_create_task(arkreen_collect_and_log_device_info(hass))
        # Setup subsequent periodic tasks
        #async_track_time_interval(hass, lambda now: schedule_periodic_task(now, hass), timedelta(seconds=10))
        async_track_time_interval(hass, schedule_periodic_task, interval)
    
    # Schedule the above-defined one-time task to run 10 seconds after Home Assistant starts
    async_call_later(hass, 10, initial_delay_callback)

    return True



    
async def get_devices_with_entities(hass, print_info=True):
    # 获取设备注册表和实体注册表
    device_reg = async_get_device_registry(hass)
    entity_reg = async_get_entity_registry(hass)

    # 创建一个列表来存储结果
    devices_with_entities = []

    # 遍历所有设备
    for device_entry in device_reg.devices.values():
        device_name = device_entry.name or device_entry.id  # 使用设备名称，如果不存在则使用ID
        device_id = device_entry.id
        device_identifiers = ', '.join(f"{id_tuple[0]}:{id_tuple[1]}" for id_tuple in device_entry.identifiers) or 'N/A'
        
        # 初始化设备条目
        device_data = {
            "name": device_name,
            "id": device_id,
            "identifier": device_identifiers,
            "entity_power": None,
            "entity_energy": None
        }

        # 查找与设备关联的所有实体
        entities = [
            entity_entry for entity_entry in entity_reg.entities.values()
            if entity_entry.device_id == device_entry.id
        ]
        
        # 查找具有 power 和 energy device_class 的实体
        for entity in entities:
            state = hass.states.get(entity.entity_id)
            if state and state.attributes.get('device_class') == 'power':
                device_data["entity_power"] = entity.entity_id
            elif state and state.attributes.get('device_class') == 'energy':
                device_data["entity_energy"] = entity.entity_id

        # 只添加有 power 或 energy 实体的设备到结果中
        if device_data["entity_power"] or device_data["entity_energy"]:
        #if device_data["name"]:
            devices_with_entities.append(device_data)

            # 如果设置了打印信息，则输出设备和它的实体及其全部信息
            if print_info:
                print(f"Device: {device_name}")
                print(f"  id: {device_id}")
                print(f"  Identifier: {device_identifiers}")
                if device_data["entity_power"]:
                    print(f"  Entity Power: {device_data['entity_power']}")
                else:
                    print("  No power entity found.")
                if device_data["entity_energy"]:
                    print(f"  Entity Energy: {device_data['entity_energy']}")
                else:
                    print("  No energy entity found.")

    return devices_with_entities

     
async def arkreen_collect_and_log_device_info(hass):
    """Collect and log info for all devices."""
    #_LOGGER.error("store arkreen timed Collected device info:")
    #entity_reg = entity_registry.async_get(hass)
    #device_reg = device_registry.async_get(hass)
    
    #await get_devices_with_entities(hass)	

    '''
    all_entities = hass.states.async_all()
    for entity in all_entities:
        print(f"arkreen Entity: {entity.entity_id}")
        state = hass.states.get(entity.entity_id)
    
        if state is None:
            print(f"Entity {entity.entity_id} not found.")
            return
    
        # 打印实体ID和状态
        print(f"  Entity ID: {state.entity_id}")
        print(f"  State: {state.state}")

        # 列出所有的属性
        print("  Attributes:")
        for attr, value in state.attributes.items():
            print(f"    {attr}: {value}")
    '''
    plant_id = hass.data.get(DOMAIN)
    if plant_id:
        _LOGGER.info(f"plant_id for {DOMAIN}: {plant_id}")
        data = plant_id['data']
        if data:
            devices = await get_devices_with_entities(hass)
            
            print(f"arkreen.State: {devices}")
            for device, details in data.items():
                id = device.split('-', 1)[1]
                plant_id = details.get('plant_id')
                owner = details.get('owner')
                matched_item = []
                try:
                    matched_item = next(item for item in devices if item['identifier'] == id)
                    _LOGGER.info(f"Entity Power: {matched_item['entity_power']}")
                    _LOGGER.info(f"Entity Energy: {matched_item['entity_energy']}")
                except StopIteration:
                    print("No matching items found.", matched_item)
       
                if not device or not plant_id or not owner:     
            	    continue
                power = None
                energy = None
                power = hass.states.get(matched_item['entity_power'])
                energy = hass.states.get(matched_item['entity_energy'])
                print(f"  power: {power.state}, energy: {energy.state}")
                #await send_rpc_data(hass, plant_id, device, power.state, energy.state)
                await send_push_data(hass, plant_id, owner, power.state, energy.state)
    pass

