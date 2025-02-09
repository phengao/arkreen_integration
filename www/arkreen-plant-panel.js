import "https://unpkg.com/wired-card@2.1.0/lib/wired-card.js?module";
import {
  LitElement,
  html,
  css,
} from "https://unpkg.com/lit-element@2.4.0/lit-element.js?module";

class ArkreenPlantPanel extends LitElement {
  static get properties() {
    return {
      page: { type: String },
      plants: { type: Array },
      devices: { type: Array }, 
      submitting: { type: Boolean }, 
      resultMessage: { type: String },
      hass: { type: Object } 
    };
  }

  constructor() {
    super();
    this.page = 'main';
    this.plants = [];
    this.devices = []; 
    this.sensorsEnergy = [];
    this.sensorsPower = [];
    this.sensorsEnergyByDevice = [];
    this.sensorsPowerByDevice = [];
    this.submitting = false;
    this.resultMessage = '';
  }

  firstUpdated() {
    this._fetchPlantInfo();
    this._fetchDevices(); // 获取设备列表
    this._fetchSensorsEnergy();
    this._fetchSensorsPower();
  }

  async _fetchDevices() {
   try {

        // 调用集成中的服务以更新设备信息
        await this.hass.callService('arkreen', 'get_devices_with_entities', {});
        

        // 等待片刻以确保服务已执行并更新了状态实体
        await new Promise(resolve => setTimeout(resolve, 500)); // 可选，根据实际情况调整

        // 获取最新的设备信息
        const response = await this.hass.callApi('GET', `arkreen/devices_with_entities`);
        console.info('    response:', JSON.stringify(response, null, 2));
        if (!response) {
            throw new Error('Failed to fetch devices with entities');
        }

        // 解析设备信息
        let devices = response;

        // 如果返回的是字符串而不是数组，请先将其转换为数组
        if (typeof devices === 'string') {
            devices = JSON.parse(devices);
        }

        console.info('    json:', JSON.stringify(devices, null, 2));

        // 
        this.devices = Object.keys(devices).map(key => `${devices[key].name}-${devices[key].identifier}`);
        console.info('    this.device:', this.devices);

        // 
        this.requestUpdate(); // 
    } catch (error) {
        console.error('Error updating device list:', error);
    }
  }

  async _fetchSensorsByDevice(device) {
   try {

        // 调用集成中的服务以更新设备信息
        //let config = {device}
        await this.hass.callService('arkreen', 'get_sensors_by_device', {device});
        console.info('    callService: _fetchSensorsByDevice');

        // 等待片刻以确保服务已执行并更新了状态实体
        await new Promise(resolve => setTimeout(resolve, 500)); // 可选，根据实际情况调整

        // 获取最新的设备信息
        const response = await this.hass.callApi('GET', `arkreen/get_sensors_by_device`);
        console.info('    response:', JSON.stringify(response, null, 2));
        if (!response) {
            throw new Error('Failed to fetch devices with entities');
        }

        // 解析设备信息
        let sensors = response;
        /*
        response ={
          'energy': [...],
          'power': [...]
        }
        */

        // 如果返回的是字符串而不是数组，请先将其转换为数组
        if (typeof sensors === 'string') {
            sensors = JSON.parse(sensors);
        }

        console.info('    json:', JSON.stringify(sensors, null, 2));

        // 
        this.sensorsEnergyByDevice = Object.keys(sensors.energy).map(key => `${sensors.energy[key]}`);
        console.info('    this.sensorsEnergyByDevice:', this.sensorsEnergyByDevice);
        this.sensorsPowerByDevice = Object.keys(sensors.power).map(key => `${sensors.power[key]}`);
        console.info('    this.sensorsPowerByDevice:', this.sensorsPowerByDevice);

        // 
        this.requestUpdate(); // 
    } catch (error) {
        console.error('Error updating sensorsEnergy list:', error);
        this.sensorsPowerByDevice = [];
        this.sensorsEnergyByDevice = [];
    }
  }

  async _fetchSensorsEnergy() {
   try {

        // 调用集成中的服务以更新设备信息
        await this.hass.callService('arkreen', 'get_sensors_energy', {});
        console.info('    callService:');

        // 等待片刻以确保服务已执行并更新了状态实体
        await new Promise(resolve => setTimeout(resolve, 500)); // 可选，根据实际情况调整

        // 获取最新的设备信息
        const response = await this.hass.callApi('GET', `arkreen/get_sensors_energy`);
        console.info('    response:', JSON.stringify(response, null, 2));
        if (!response) {
            throw new Error('Failed to fetch devices with entities');
        }

        // 解析设备信息
        let sensors = response;

        // 如果返回的是字符串而不是数组，请先将其转换为数组
        if (typeof sensors === 'string') {
            sensors = JSON.parse(sensors);
        }

        console.info('    json:', JSON.stringify(sensors, null, 2));

        // 
        this.sensorsEnergy = Object.keys(sensors).map(key => `${sensors[key]}`);
        console.info('    this.sensorsEnergy:', this.sensorsEnergy);

        // 
        this.requestUpdate(); // 
    } catch (error) {
        console.error('Error updating sensorsEnergy list:', error);
    }
  }

  async _fetchSensorsPower() {
   try {

        // 调用集成中的服务以更新设备信息
        await this.hass.callService('arkreen', 'get_sensors_power', {});
        

        // 等待片刻以确保服务已执行并更新了状态实体
        await new Promise(resolve => setTimeout(resolve, 500)); // 可选，根据实际情况调整

        // 获取最新的设备信息
        const response = await this.hass.callApi('GET', `arkreen/get_sensors_power`);
        console.info('    response:', JSON.stringify(response, null, 2));
        if (!response) {
            throw new Error('Failed to fetch snesors of power');
        }

        // 解析设备信息
        let sensors = response;

        // 如果返回的是字符串而不是数组，请先将其转换为数组
        if (typeof sensors === 'string') {
            sensors = JSON.parse(sensors);
        }

        console.info('    json:', JSON.stringify(sensors, null, 2));

        // 
        this.sensorsPower = Object.keys(sensors).map(key => `${sensors[key]}`);
        console.info('    this.sensorsPower:', this.sensorsPower);

        // 
        this.requestUpdate(); // 
    } catch (error) {
        console.error('Error updating snesorsPower list:', error);
    }
  }
  
  async handleFormSubmit(event) {
    event.preventDefault(); // Prevent the default form submission behavior
  
    this.submitting = true;  // Set submitting state to true
    this.resultMessage = 'Submiting...';
    this.requestUpdate();  // Force re-render to update button state
  
    const form = event.target;
    const formData = new FormData(form);
    
    let hasEmptyField = false;
    for (let [key, value] of formData.entries()) {
      if (!value.trim()) {
        hasEmptyField = true;
        break;
      }
    }
  
    if (hasEmptyField) {
      alert('Please fill in all fields');
      this.submitting = false;  // If validation fails, reset submitting state
      this.requestUpdate();
      return;
    }
  

    
    let rpc_request_body = {
      "jsonrpc": "2.0",
      "method": "receiveData",
      "params": {},  // 初始化为空对象
      "id": 1
    };

    formData.forEach((value, key) => {
      rpc_request_body.params[key] = value;
    });
    
    console.info("fetch body:", JSON.stringify(rpc_request_body));
    const url = "http://192.168.71.34:19812/asp/homeassistant/push";
    //const url = 'http://192.168.71.34:3000/rpc';
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(rpc_request_body)
      });
      
      const data = await response.json();
      this.resultMessage = data.message || 'Submission successful';
    } catch (error) {
      console.error('Error:', error);
      this.resultMessage = 'Submission failed';
    } finally {
      this.submitting = false;  // Reset submitting state regardless of success or failure
      this.requestUpdate();  // Force re-render to update button state
    }
  }
  
  async handleChange(event) {
    const selectedDevice = event.target.value;
    console.info("handle change:", selectedDevice);
    if (selectedDevice) {
      this._fetchSensorsByDevice(selectedDevice);
    } else {
      this.sensorsEnergyByDevice = [];
      this.sensorsPowerByDevice = [];
    }
  }

  async handleFormApplicationSubmit(event) {
    event.preventDefault(); // Prevent the default form submission behavior
  
    this.submitting = true;  // Set submitting state to true
    this.resultMessage = 'Submiting...';
    this.requestUpdate();  // Force re-render to update button state
  
    const form = event.target;
    const formData = new FormData(form);
    
    let hasEmptyField = false;
    for (let [key, value] of formData.entries()) {
      if (!value.trim()) {
        hasEmptyField = true;
        break;
      }
    }
  
    if (hasEmptyField) {
      alert('Please fill in all fields');
      this.submitting = false;  // If validation fails, reset submitting state
      this.requestUpdate();
      return;
    }
  

    
    let rpc_request_body = {
      "jsonrpc": "2.0",
      "method": "receiveData",
      "params": {},  // 初始化为空对象
      "id": 1
    };

    formData.forEach((value, key) => {
      rpc_request_body.params[key] = value;
    });
    
    console.info("fetch body:", JSON.stringify(rpc_request_body));
    //const url = "http://192.168.71.34:19812/asp/homeassistant/push";
    //const url = 'http://192.168.71.34:3000/rpc';
    try {
      // 调用服务
      //await hass.callService('arkreen', serviceName, serviceData);
      await this.hass.callService('arkreen', 'send_plant_application', rpc_request_body);
    
      // 定义轮询函数
      const maxAttempts = 10;
      const pollForResult = async (entityId, maxAttempts = 10, intervalMs = 2000) => {
        let attempt = 0;
      
        while (attempt < maxAttempts) {
          attempt++;
        
          // 等待一段时间再进行下一次请求
          await new Promise(resolve => setTimeout(resolve, 100));
        
          // 获取实体状态
          const response = await this.hass.callApi('GET', `states/${entityId}`);
          console.info(`Attempt ${attempt}:`, JSON.stringify(response, null, 2));

          // 检查是否已得到结果
          if (response && response.state !== 'pending') { // 假设'pending'为未完成状态
            console.info('Result obtained:', response.attributes.result);
            return response.attributes.result; // 返回结果
          }
        }

        throw new Error('Max attempts reached without getting the result');
      };

      // 开始轮询
      const entityId = 'arkreen.sendplantapplication'; // 替换为实际用于存储结果的实体ID
      const result = await pollForResult(entityId);

      this.resultMessage = 'Submission successful: ' + result;
      return result;
    } catch (error) {
      console.error('Error calling service or polling for result:', error);
      this.resultMessage = 'Submission failed';
    } finally {
      this.submitting = false;  // Reset submitting state regardless of success or failure
      this.requestUpdate();  // Force re-render to update button state
    }
  }

  async handleFormActiveSubmit(event) {
    event.preventDefault(); // Prevent the default form submission behavior
  
    this.submitting = true;  // Set submitting state to true
    this.resultMessage = 'Submiting...';
    this.requestUpdate();  // Force re-render to update button state
  
    const form = event.target;
    const formData = new FormData(form);
    
    let hasEmptyField = false;
    for (let [key, value] of formData.entries()) {
      if (!value.trim()) {
        hasEmptyField = true;
        break;
      }
    }
  
    if (hasEmptyField) {
      alert('Please fill in all fields');
      this.submitting = false;  // If validation fails, reset submitting state
      this.requestUpdate();
      return;
    }
  

    
    let config = {};

    formData.forEach((value, key) => {
      config[key] = value;
    });
    
    console.log('Saving configuration...');
    /*
    const config = {
      device: this.selectedDevice,
      plant_id: this.devicePlantId,
      owner: this.ownerInfo
      entity_energy = call.data.get('entity_energy')
      entity_power = call.data.get('entity_power')
    };
    */
    try {
      // Call the Home Assistant service to save the configuration
      await this.hass.callService('arkreen', 'save_config', config);

      console.log('Configuration saved successfully', config);
      this.resultMessage = 'Active successful';
    } catch (error) {
      console.error('Failed to save configuration:', error);
      console.error('Error calling service or polling for result:', error);
      this.resultMessage = 'Submission failed';
    } finally {
      this.submitting = false;  // Reset submitting state regardless of success or failure
      this.requestUpdate();  // Force re-render to update button state
    }
  }  

  render() {
    return html`
      <h1>Arkreen Plant:</h1>

      ${this.page === 'main' ? this._renderMainPage() : ''}

      ${this.page === 'apply' ? this._renderApplyForm() : ''}

      ${this.page === 'activate' ? this._renderActivateForm() : ''}
    `;
  }

  _renderMainPage() {
    return html`
      <p>Currently owned Arkreen Plants</p>
      <hr style="width: 100%;">
      ${this.plants.length > 0 ? html`
          <table style="border-collapse: collapse; border: 1px solid black;">
              <thead>
                  <tr style="border: 1px solid black;">
                      <th style="border: 1px solid black;">name</th>
                      <th style="border: 1px solid black;">plant_id</th>
                      <th style="border: 1px solid black;">owner</th>
                      <th style="border: 1px solid black;">entity_energy</th>
                      <th style="border: 1px solid black;">entity_power</th>
                  </tr>
              </thead>
              <tbody>
                 ${this.plants.map(plant => html`
                      <tr style="border: 1px solid black;">
                         <td style="border: 1px solid black;">${plant.name}</td>
                         <td style="border: 1px solid black;">${plant.plant_id}</td>
                         <td style="border: 1px solid black;">${plant.owner}</td>
                         <td style="border: 1px solid black;">${plant.entity_energy}</td>
                         <td style="border: 1px solid black;">${plant.entity_power}</td>
                      </tr>
                  `)}
              </tbody>
          </table>
      ` : html`<p>No plant information available.</p>`}
      <hr>
      <button @click=${() => this._showPage('apply')}>Apply for Plant</button> <p>Fill in the application form for a new plant.</p>
      <button @click=${() => this._showPage('activate')}>Activate Plant</button>
      <p>Activate an applied plant after receiving approval.</p>
    `;
  }

  _renderApplyForm() {
    return html`
      <p>Fill in the application form for a new plant</p>
      <hr style="width: 100%;">
      <form id="applyForm" @submit=${this.handleFormApplicationSubmit} style="display:flex;flex-direction:column;"
        <!-- Form fields aligned with specified proportions -->
        <div style="display:flex;justify-content:center;">
          <label style="flex: 0 1 calc(25% - 10px);">Select Device :</label>
          <select name="device" id="device" style="flex: 0 1 calc(33.333% - 30px);">
            <option value="">Select a device</option>
            ${this.devices.map(deviceName => html`
              <option value="${deviceName}">${deviceName}</option>
            `)}
          </select>
        </div><br>
        <div style="display:flex;justify-content:center;">
          <label style="flex: 0 1 calc(25% - 10px);">RatedPower :</label>
          <input type="text" name="ratedpower" id="ratedpower" value="1000" style="flex: 0 1 calc(33.333% - 30px);">
        </div><br>
        <div style="display:flex;justify-content:center;">
          <label style="flex: 0 1 calc(25% - 10px);">Username :</label>
          <input type="text" name="username" id="username" value="your name" style="flex: 0 1 calc(33.333% - 30px);">
        </div><br>
        <div style="display:flex;justify-content:center;">
          <label style="flex: 0 1 calc(25% - 10px);">Email Address :</label>
          <input type="email" name="email" id="email" value="your@email" style="flex: 0 1 calc(33.333% - 30px);">
        </div><br>
        <div style="display:flex;justify-content:center;">
          <label style="flex: 0 1 calc(25% - 10px);">Social Account :</label>
          <input type="text" name="social" id="social" value="your social" style="flex: 0 1 calc(33.333% - 30px);">
        </div><br>
        <div style="display:flex;justify-content:center;">
          <label style="flex: 0 1 calc(25% - 10px);">Phone Number :</label>
          <input type="tel" name="phone" id="phone" value="401231" style="flex: 0 1 calc(33.333% - 30px);">
        </div><br>
        <div style="display:flex;justify-content:center;">
          <label style="flex: 0 1 calc(25% - 10px);">Owner Address :</label>
          <input type="text" name="ownerAddress" id="ownerAddress" value="0x259df9c21d8a7F716C26dF1259D7FDCab96E722E" style="flex: 0 1 calc(33.333% - 30px);">
        </div><br>
        <div style="display:flex;justify-content:center;">
          <label style="flex: 0 1 calc(25% - 10px);">Country/Region :</label>
          <input type="text" name="country" id="country" value="Germany" style="flex: 0 1 calc(33.333% - 30px);">
        </div><br>
        <div style="display:flex;justify-content:center;">
          <label style="flex: 0 1 calc(25% - 10px);">City :</label>
          <input type="text" name="city" id="city" value="Frankfurt" style="flex: 0 1 calc(33.333% - 30px);">
        </div><br>
        <hr style="width: 100%;">
        <div style="display:flex;justify-content:space-between;">
          <button @click=${() => this._showPage('main')} style="width: 150px;">Back</button>
          <button 
            type="submit" 
            style="width: 150px;"
            ?disabled=${this.submitting}
            >
            ${this.submitting ? 'Submitting...' : 'Submit Application'}
          </button>
        </div><br>
        <!-- show response -->
        ${this.resultMessage ? html`<p>${this.resultMessage}</p>` : ''}
      </form>
    `;
  }

  _renderActivateForm() {
    return html`
      <p>Activate an applied plant after receiving approval</p>
      <hr style="width: 100%;">
      <form id="activateForm" @submit=${this.handleFormActiveSubmit} style="display:flex;flex-direction:column;">
        <div style="display:flex;justify-content:center;">
          <label style="flex: 0 1 calc(25% - 10px);">Select Device :</label>
          <select name="device" id="device" style="flex: 0 1 calc(33.333% - 30px);" @change="${(event) => this.handleChange(event)}">
            <option value="">Select a device</option>
            ${this.devices.map(deviceName => html`
              <option value="${deviceName}">${deviceName}</option>
            `)}
          </select>
        </div><br>
        <div style="display:flex;justify-content:center;">
          <label style="flex: 0 1 calc(25% - 10px);">Select Energy Entity :</label>
          <select name="entity_energy" id="entity_energy" style="flex: 0 1 calc(33.333% - 30px);">
            <option value="">Select a energySensor</option>
            ${this.sensorsEnergyByDevice.map(deviceName => html`
              <option value="${deviceName}">${deviceName}</option>
            `)}
          </select>
        </div><br>
        <div style="display:flex;justify-content:center;">
          <label style="flex: 0 1 calc(25% - 10px);">Select Power Entity :</label>
          <select name="entity_power" id="entity_power" style="flex: 0 1 calc(33.333% - 30px);">
            <option value="">Select a powerSensor</option>
            ${this.sensorsPowerByDevice.map(deviceName => html`
              <option value="${deviceName}">${deviceName}</option>
            `)}
          </select>
        </div><br>
        <div style="display:flex;justify-content:center;">
          <label style="flex: 0 1 calc(25% - 10px);">Plant ID :</label>
          <input type="text" name="plant_id" id="plant_id" style="flex: 0 1 calc(33.333% - 30px);">
        </div><br>
        <div style="display:flex;justify-content:center;">
          <label style="flex: 0 1 calc(25% - 10px);">Owner Address :</label>
          <input type="text" name="owner" id="owner" value="0x259df9c21d8a7F716C26dF1259D7FDCab96E722E" style="flex: 0 1 calc(33.333% - 30px);">
        </div><br>
        <hr style="width: 100%;">
        <div style="display:flex;justify-content:space-between;">
          <button @click=${() => this._showPage('main')}  style="width: 150px;">Back</button>
          <button type="submit" style="width: 150px;">Activate Plant</button>
        </div><br>
        <!-- show response -->
        ${this.resultMessage ? html`<p>${this.resultMessage}</p>` : ''}        

      </form>
    `;
  }

  _showPage(page) {
    this.page = page;
    this.resultMessage = '';
    this._fetchPlantInfo();
    this.sensorsPowerByDevice = [];
    this.sensorsEnergyByDevice = [];
  }

  async _fetchPlantInfo() {
   try {

        // 调用集成中的服务以更新设备信息
        //await this.hass.callService('arkreen', 'get_plant_info', {});
        

        // 等待片刻以确保服务已执行并更新了状态实体
        //await new Promise(resolve => setTimeout(resolve, 500)); // 可选，根据实际情况调整

        // 获取最新的设备信息
        const response = await this.hass.callApi('GET', `arkreen/plants_data`);
        console.info('    response:', JSON.stringify(response, null, 2));
        if (!response) {
            throw new Error('Failed to fetch plants data');
        }

        // 解析设备信息
        let plants = response;

        // 如果返回的是字符串而不是数组，请先将其转换为数组
        if (typeof plants === 'string') {
            plants = JSON.parse(plants);
        }

        console.info('    json:', JSON.stringify(plants, null, 2));

        // 
        this.plants = plants;
        console.info('    this.plants:', this.plants);

        // 
        //this.requestUpdate(); // 
    } catch (error) {
      console.error('Failed to fetch plant info:', error);
      this.plants = [];
    }
  } 
}

customElements.define('arkreen-plant-panel', ArkreenPlantPanel);
