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
        _LOGGER.error("get devices_with_entities: %s", devices_with_entities)

        return web.json_response(devices_with_entities)

class SensorsByDeviceView(HomeAssistantView):
    """View to handle sensors of device requests."""

    url = f"/api/{DOMAIN}/get_sensors_by_device"
    name = f"api:{DOMAIN}:get_sensors_by_device"

    async def get(self, request):
        """Handle GET request for sensor of device."""
        hass = request.app['hass']
        domain_data = hass.data.get(DOMAIN, {})
        sensors_by_device = domain_data.get('sensors_by_device', [])
        _LOGGER.error("get sensors_by_device: %s", sensors_by_device)

        return web.json_response(sensors_by_device)


class SensorsEnergyView(HomeAssistantView):
    """View to handle sensor of energy requests."""

    url = f"/api/{DOMAIN}/get_sensors_energy"
    name = f"api:{DOMAIN}:get_sensors_energy"

    async def get(self, request):
        """Handle GET request for sensor of energy."""
        hass = request.app['hass']
        domain_data = hass.data.get(DOMAIN, {})
        sensors_energy = domain_data.get('sensors_energy', [])
        _LOGGER.error("get sensors_energy: %s", sensors_energy)

        return web.json_response(sensors_energy)

class SensorsPowerView(HomeAssistantView):
    """View to handle sensor of power requests."""

    url = f"/api/{DOMAIN}/get_sensors_power"
    name = f"api:{DOMAIN}:get_sensors_power"

    async def get(self, request):
        """Handle GET request for sensor of power."""
        hass = request.app['hass']
        domain_data = hass.data.get(DOMAIN, {})
        sensors_power = domain_data.get('sensors_power', [])
        _LOGGER.error("get sensors_power: %s", sensors_power)

        return web.json_response(sensors_power)

class PlantsDataView(HomeAssistantView):
    """View to handle devices with entities requests."""

    url = f"/api/{DOMAIN}/plants_data"
    name = f"api:{DOMAIN}:plants_data"

    async def get(self, request):
        """Handle GET request for devices with entities."""
        hass = request.app['hass']
        domain_data = hass.data.get(DOMAIN, {})
        plants_data = domain_data.get('data', [])
        _LOGGER.error("get plants_data: %s", plants_data)
        plants = []
        for name, details in plants_data.items():
          plant_info = {
            'name': name,
            'plant_id': details['plant_id'],
            'owner': details['owner'],
            'entity_power': details['entity_power'],
            'entity_energy': details['entity_energy']
          }
          plants.append(plant_info)

        return web.json_response(plants)
        
async def send_push_data(hass: HomeAssistant, plant_id: str, owner: str, power: str, energy: str):
    #url = "http://192.168.71.70:3000/hapush"
    url = "http://192.168.71.70:19812/asp/homeassistant/push"
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

async def send_plant_application_list(hass: HomeAssistant, data):
    #url = "http://192.168.71.70:3000/hapush"
    url = "http://192.168.71.70:19812/asp/homeassistant/push"
    headers = {'Content-Type': 'application/json'}

    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers={'Content-Type': 'application/json'}, json=data) as response:
                if response.status == 200:
                    _LOGGER.info("spal Data sent successfully.")
                    response_json = await response.text()
                    _LOGGER.info("spal Response from server: %s", response_json)
                    return response_json
                else:
                    _LOGGER.error("spal Failed to send data. Status code: %d", response.status)
                    text = await response.text()
                    _LOGGER.error("spal Response body: %s", text)
                    return text
    except aiohttp.ClientError as err:
        _LOGGER.error("Error send_plant_application_list: %s", err)
        return err
# 定义要发送的数据结构
RPC_URL = "http://192.168.71.70:3000/rpc"  # 替换为实际的RPC接口URL
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
    #await arkreen_collect_and_log_device_info(hass)
    await arkreen_plant_timed_update(hass)
    pass



async def async_setup(hass, config):
    """Set up the example integration."""  

    # 注册新的RESTful API端点
    hass.http.register_view(DevicesWithEntitiesView())    
    hass.http.register_view(SensorsEnergyView())    
    hass.http.register_view(SensorsPowerView())    
    hass.http.register_view(PlantsDataView())    
    hass.http.register_view(SensorsByDeviceView())    
    
    
     
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
        entity_energy = call.data.get('entity_energy')
        entity_power = call.data.get('entity_power')

        if not device or not plant_id or not owner:
            _LOGGER.error(f"ark All fields are required", config)
            return

        # 检查设备是否已存在
        current_time_stamp = str(int(asyncio.get_event_loop().time()))  # 使用事件循环的时间作为时标
        if device in hass.data[DOMAIN]['data']:
            original_device = device
            device += "_" + current_time_stamp  # 修改设备名称为device+当前时标
            _LOGGER.info(f"Device {original_device} already exists, renaming to {device}")

    
        # Save new configuration to data
        hass.data[DOMAIN]['data'][device] = {
            'plant_id': plant_id,
            'owner': owner,
            'entity_power': entity_power,
            'entity_energy': entity_energy
        }

        # Write data back to storage
        await hass.data[DOMAIN]['store'].async_save(hass.data[DOMAIN]['data'])

        _LOGGER.info(f"Configuration for {device} saved.")

        _LOGGER.error("arkreen Configuration saved: %s", config)
    
    hass.services.async_register(DOMAIN, 'save_config', _handle_save_config_service)

    async def _handle_get_devices_with_entities_service(call: ServiceCall):
        result = await get_devices_with_entities(hass)
        print(f"  result: {result}")
        hass.data.setdefault(DOMAIN, {})['devices_with_entities'] = result
        return result
        
    hass.services.async_register(DOMAIN, 'get_devices_with_entities', _handle_get_devices_with_entities_service)

    async def _handle_get_sensors_by_device_service(call: ServiceCall):
        print(f'by device:%s', call.data)
        device = call.data.get('device')
        result = await get_sensors_by_device(hass, device)
        print(f"  result: {result}")
        hass.data.setdefault(DOMAIN, {})['sensors_by_device'] = result
        return result
        
    hass.services.async_register(DOMAIN, 'get_sensors_by_device', _handle_get_sensors_by_device_service)

    async def _handle_get_sensors_energy_service(call: ServiceCall):
        result = await get_sensors_energy(hass)
        print(f"  result: {result}")
        hass.data.setdefault(DOMAIN, {})['sensors_energy'] = result
        return result
        
    hass.services.async_register(DOMAIN, 'get_sensors_energy', _handle_get_sensors_energy_service)
    
    async def _handle_get_sensors_power_service(call: ServiceCall):
        result = await get_sensors_power(hass)
        print(f"  result: {result}")
        hass.data.setdefault(DOMAIN, {})['sensors_power'] = result
        return result
        
    hass.services.async_register(DOMAIN, 'get_sensors_power', _handle_get_sensors_power_service)

    async def _handle_send_plant_application_service(call: ServiceCall):
        """Handle the service call."""
        # Extract parameters from the service call
        config = call.data.get('params')
        print(f"send_plant_application: {config}")        
        hass.states.async_set("arkreen.sendplantapplication", "pending", {'progress': 'Starting...'})
        response = await send_plant_application_list(hass, config)

        hass.states.async_set('arkreen.sendplantapplication', 'completed', {'result': response})

        print(f"spa response: {response}")
        
    hass.services.async_register(DOMAIN, 'send_plant_application', _handle_send_plant_application_service)
           
    # 创建一个时间间隔调度器，例如每1分钟执行一次
    interval = timedelta(seconds = 60)
    
    @callback
    def schedule_periodic_task(now):
        """Schedule the periodic task."""
        hass.async_create_task(my_periodic_function(hass, now))

    # Define a one-time task that will be executed after a 10-second delay
    async def initial_delay_callback(event_time):
        # Execute the task you want to run immediately once
        #hass.async_create_task(arkreen_collect_and_log_device_info(hass))
        hass.async_create_task(arkreen_plant_timed_update(hass))
        async_track_time_interval(hass, schedule_periodic_task, interval)
    
    # Schedule the above-defined one-time task to run 10 seconds after Home Assistant starts
    async_call_later(hass, 10, initial_delay_callback)

    return True

async def get_sensors_energy(hass, print_info=True):
    # 获取设备注册表和实体注册表
    entity_reg = async_get_entity_registry(hass)
    sensor_energy = []

    for entity_entry in entity_reg.entities.values():
        state = hass.states.get(entity_entry.entity_id)
        print(f"states.get: {entity_entry.entity_id}")
        if state and state.attributes.get('device_class') == 'energy':
            sensor_energy.append(entity_entry.entity_id)
            if print_info:
                print(f"Energy Sensor: {entity_entry.entity_id}")

    return sensor_energy


async def get_sensors_power(hass, print_info=True):
    # 获取设备注册表和实体注册表
    entity_reg = async_get_entity_registry(hass)
    sensor_power = []

    for entity_entry in entity_reg.entities.values():
        state = hass.states.get(entity_entry.entity_id)
        if state and state.attributes.get('device_class') == 'power':
            sensor_power.append(entity_entry.entity_id)
            if print_info:
                print(f"Power Sensor: {entity_entry.entity_id}")

    return sensor_power

async def get_sensors_by_device(hass, device, print_info = True):
    device_reg = async_get_device_registry(hass)
    entity_reg = async_get_entity_registry(hass)

    # 创建一个列表来存储结果
    sensors_by_device = {'energy': [], 'power': []}
    
    identifier = device.split('-', 1)[1]
    _LOGGER.info("  indentifier: %s", identifier)

    # 遍历所有设备
    for device_entry in device_reg.devices.values():
        device_name = device_entry.name or device_entry.id  # 使用设备名称，如果不存在则使用ID
        device_id = device_entry.id
        device_identifiers = ', '.join(f"{id_tuple[0]}:{id_tuple[1]}" for id_tuple in device_entry.identifiers) or 'N/A'
        if device_identifiers == identifier:
            # 查找与设备关联的所有实体
            entities = [
                entity_entry for entity_entry in entity_reg.entities.values()
                if entity_entry.device_id == device_entry.id
            ]

            # 查找具有 power 和 energy device_class 的实体
            for entity in entities:
                state = hass.states.get(entity.entity_id)
                if state and state.attributes.get('device_class') == 'power':
                    sensors_by_device['power'].append(entity.entity_id)
                    #device_data["entity_power"] = entity.entity_id
                elif state and state.attributes.get('device_class') == 'energy':
                    sensors_by_device['energy'].append(entity.entity_id)
                    #device_data["entity_energy"] = entity.entity_id            
            
            if print_info:
                print(f"Device: {device_name}")
                print(f"  id: {device_id}")
                print(f"  Identifier: {device_identifiers}")
                print(f"  power sensors: {sensors_by_device['power']}")                      
                print(f"  energy sensors: {sensors_by_device['energy']}")                      
            break;
        
    return sensors_by_device
    
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
    
async def arkreen_plant_timed_update(hass):
    """Collect and log info for all devices."""

    plant_id = hass.data.get(DOMAIN)
    if plant_id:
        _LOGGER.info(f"plant_id for {DOMAIN}: {plant_id}")
        data = plant_id['data']
        if data:
            items_list = list(data.items())
            #for device, details in data.items():
            for index in range(len(items_list)):
                device, details = items_list[index]
                id = device.split('-', 1)[1]
                plant_id = details.get('plant_id')
                owner = details.get('owner')
                entity_power = details.get('entity_power')
                entity_energy = details.get('entity_energy')
                _LOGGER.info(f"Plant ID: {plant_id}")
                _LOGGER.info(f"Entity Power: {entity_power}")
                _LOGGER.info(f"Entity Energy: {entity_energy}")

       
                if not device or not plant_id or not owner:     
            	    continue
                power = None
                energy = None
                if entity_power:
                  power = hass.states.get(entity_power)
                if entity_energy:
                  energy = hass.states.get(entity_energy)
                  print(f"  {plant_id} power: {power.state}, energy: {energy.state}")
                  dev = device.replace('-', '_').replace(':', '_').replace(' ','_')
                  hass.states.async_set(f"arkreen.{dev}", f"{power.state} W, {energy.state} kWh")
                  await send_push_data(hass, plant_id, owner, power.state, energy.state)
                  _LOGGER.info(f"  sleep 0")
                  await asyncio.sleep(0.5)
                  _LOGGER.info(f"  sleep 0.5")
    pass

