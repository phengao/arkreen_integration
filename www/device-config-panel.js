import "https://unpkg.com/wired-card@2.1.0/lib/wired-card.js?module";
import {
  LitElement,
  html,
  css,
} from "https://unpkg.com/lit-element@2.4.0/lit-element.js?module";

class DeviceConfigPanel extends LitElement {
  static get properties() {
    return {
      hass: { type: Object },
      narrow: { type: Boolean },
      route: { type: Object },
      panel: { type: Object },
      selectedDevice: { type: String },
      devicePlantId: { type: String },
      ownerInfo: { type: String }
    };
  }

  constructor() {
    super();
    this.selectedDevice = '';
    this.devicePlantId = '';
    this.ownerInfo = '';
  }

  // Fetch the list of devices when the element is first connected to the DOM.
  connectedCallback() {
    super.connectedCallback();
    this.updateDeviceList();
  }

  async updateDeviceList() {
    try {
        /*
        const devices = await this.hass.callApi('GET', 'states');
        console.info('    this.device:', devices);

        this.devices = Object.keys(devices).map(key => devices[key].entity_id);
        */    
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

        // 提取设备名称用于下拉菜单
        this.devices = Object.keys(devices).map(key => `${devices[key].name}-${devices[key].identifier}`);
        /*
        this.devices = devices.map(device => ({
            name: device.name,
            id: device.id,
            identifier: device.identifier,
            entity_power: device.entity_power,
            entity_energy: device.entity_energy,
            displayText: `${device.name}-${device.identifier}` 
        }));
        */

        console.info('    this.device:', this.devices);

        // 更新下拉菜单或其他UI元素
        this.requestUpdate(); // 触发渲染周期以显示新数据
    } catch (error) {
        console.error('Error updating device list:', error);
    }
  }

  handleDeviceChange(e) {
    this.selectedDevice = e.target.value;
  }

  handlePlantIdChange(e) {
    this.devicePlantId = e.target.value;
  }
  handleOwnerChange(e) {
    this.ownerInfo = e.target.value;
  }

  async saveConfiguration() {
    // Here you would implement your logic for saving the configuration.
    // This could be writing to a local file, sending to a server, etc.
    console.log('Saving configuration...');
    const config = {
      device: this.selectedDevice,
      plant_id: this.devicePlantId,
      owner: this.ownerInfo
    };

    try {
      // Call the Home Assistant service to save the configuration
      await this.hass.callService('arkreen', 'save_config', config);

      console.log('Configuration saved successfully', config);
    } catch (error) {
      console.error('Failed to save configuration:', error);
    }
  }

  render() {
    return html`
      <wired-card elevation="2">
        <select @change=${this.handleDeviceChange}>
          <option value="">Select a device</option>
          ${this.devices ? this.devices.map(device => html`
            <option value="${device}" ?selected=${this.selectedDevice === device}>${device}</option>
          `) : ''}
        </select>
        <label for="Plant-id">Plant ID:</label>
        <input type="text" placeholder="Enter plant id" .value=${this.devicePlantId} @input=${this.handlePlantIdChange} />
        <label for="Owner">Owner:</label>
        <input type="text" placeholder="Enter owner info" .value=${this.ownerInfo} @input=${this.handleOwnerChange} />
        <button @click=${this.saveConfiguration}>Save Configuration</button>
      </wired-card>
    `;
  }

  static get styles() {
    return css`
      :host {
        background-color: #fafafa;
        padding: 16px;
        display: block;
      }
      wired-card {
        background-color: white;
        padding: 16px;
        display: block;
        font-size: 18px;
        max-width: 600px;
        margin: 0 auto;
      }
      select, input, button {
        display: block;
        width: 100%;
        margin-bottom: 10px;
      }
    `;
  }
}

customElements.define("device-config-panel", DeviceConfigPanel);
