<script setup>
import { ref, computed, onMounted } from 'vue';
import axios from 'axios';

// Declare reactive variables
const sensors = ref([]);
const searchQuery = ref('');
const showMetrics = ref([]);
const showTypes = ref([]);
const selectedMetric = ref('all'); 
const selectedType = ref('all'); 

const sortColumn = ref(''); // Track the current sort column
const sortOrder = ref('asc'); // Track the current sort order ('asc' or 'desc')

const fetchData = async () => {
  try {
    // Fetch sensors data
    const sensorsResponse = await axios.get('http://127.0.0.1:8000/api/sensors/');
    let sensorsData = sensorsResponse.data;
    const sensorKeys = Object.keys(sensorsData);

    // Convert sensors data into an array of Sensor objects
    let sensorsArray = sensorKeys.map(key => {
      let sensorData = sensorsData[key];
      return {
        id: key,
        metrics: sensorData.metrics,
        name: sensorData.name ? sensorData.name : `Sensor with id: ${key}`,
        type: sensorData.type,
        variant: sensorData.variant
      };
    });

    // Fetch metrics data
    const metricsResponse = await axios.get('http://127.0.0.1:8000/api/metrics/');
    const metricsData = metricsResponse.data;

    // Fetch sensor types data
    const sensorTypesResponse = await axios.get('http://127.0.0.1:8000/api/types/');
    const sensorTypes = sensorTypesResponse.data;

    let tempMetricShow = [];
    // Add metric data to sensor
    sensorsArray.forEach(sensor => {
      Object.keys(sensor.metrics).forEach(metricId => {
        const metric = metricsData.data.items.find(item => item.id === metricId);
        if (metric) {
          sensor.metrics[metricId] = {
            ...sensor.metrics[metricId],
            name: metric.name,
            units: metric.units
          };
          if (!tempMetricShow.some(item => item.id === metricId)) {
            tempMetricShow.push({
              id: metricId,
              name: metric.name
            });
          }
        }
      });
    });

    showMetrics.value = tempMetricShow;

    // Populate showTypes without duplicates
    let tempTypeShow = [];
    sensorsArray.forEach(sensor => {
      const sensorType = sensorTypes[sensor.type];
      if (sensorType) {
        const variant = sensorType[sensor.variant];
        const typeName = variant ? variant.name : 'Unknown Variant';
        if (!tempTypeShow.some(type => type.id === sensor.type)) {
          tempTypeShow.push({
            id: sensor.type,
            name: typeName
          });
        }
        sensor.typeName = typeName;
      } else {
        if (!tempTypeShow.some(type => type.id === sensor.type)) {
          tempTypeShow.push({
            id: sensor.type,
            name: 'Unknown Type'
          });
        }
        sensor.typeName = 'Unknown Type';
      }
    });
    showTypes.value = tempTypeShow;

    sensors.value = sensorsArray;

  } catch (error) {
    console.error('Error fetching data:', error);
  }
};

// Compute sorted sensors
const sortedSensors = computed(() => {
  const query = searchQuery.value.toLowerCase();
  let sensorsToSort = sensors.value
    .filter(sensor => sensor.name.toLowerCase().includes(query))
    .filter(sensor => {
      // Filter based on selectedType
      return selectedType.value === 'all' || sensor.typeName === selectedType.value;
    })
    .map(sensor => {
      let filteredMetrics;

      // Check if 'all' is selected for metrics
      if (selectedMetric.value === 'all') {
        filteredMetrics = sensor.metrics;
      } else {
        // Filter metrics based on selectedMetric
        filteredMetrics = Object.keys(sensor.metrics)
          .filter(metricId => selectedMetric.value == metricId)
          .reduce((obj, metricId) => {
            obj[metricId] = sensor.metrics[metricId];
            return obj;
          }, {});
      }

      return {
        ...sensor,
        metrics: filteredMetrics
      };
    })
    .filter(sensor => Object.keys(sensor.metrics).length > 0);

  // Sort sensors based on the selected column and order
  if (sortColumn.value) {
    sensorsToSort.sort((a, b) => {
      let aValue, bValue;

      switch (sortColumn.value) {
        case 'name':
          aValue = a.name.toLowerCase();
          bValue = b.name.toLowerCase();
          break;
        case 'typeName':
          aValue = a.typeName.toLowerCase();
          bValue = b.typeName.toLowerCase();
          break;
        case 'timestamp':
          aValue = Object.values(a.metrics)[0]?.t || 0; // Assuming you're sorting based on the first metric's timestamp
          bValue = Object.values(b.metrics)[0]?.t || 0;
          break;
        case 'value':
          aValue = Object.values(a.metrics)[0]?.v || 0; // Assuming you're sorting based on the first metric's value
          bValue = Object.values(b.metrics)[0]?.v || 0;
          break;
        case 'metricName':
          aValue = Object.values(a.metrics)[0]?.name.toLowerCase() || ''; // Metric name of the first metric
          bValue = Object.values(b.metrics)[0]?.name.toLowerCase() || '';
          break;
        case 'unitName':
          aValue = Object.values(a.metrics)[0]?.units.find(unit => unit.selected)?.name.toLowerCase() || ''; // Unit name of the first metric
          bValue = Object.values(b.metrics)[0]?.units.find(unit => unit.selected)?.name.toLowerCase() || '';
          break;
      }

      if (aValue < bValue) return sortOrder.value === 'asc' ? -1 : 1;
      if (aValue > bValue) return sortOrder.value === 'asc' ? 1 : -1;
      return 0;
    });
  }

  return sensorsToSort;
});

// Handle select change to update selectedMetric
const handleMetricChange = (event) => {
  selectedMetric.value = event.target.value;
};

// Handle select change to update selectedType
const handleTypeChange = (event) => {
  selectedType.value = event.target.value;
};

// Handle sort column change
const handleSort = (column) => {
  if (sortColumn.value === column) {
    sortOrder.value = sortOrder.value === 'asc' ? 'desc' : 'asc'; // Toggle sort order
  } else {
    sortColumn.value = column;
    sortOrder.value = 'asc'; // Default to ascending
  }
};

onMounted(() => {
  fetchData();
});
</script>

<template>
  <div>
    <h1>SAF uzdevums, autors - Artūrs Palamarčuks</h1>
    
    <!-- Search Input -->
    <div>
      <label for="search">Meklēt: </label>
      <input
        id="search"
        type="text"
        v-model="searchQuery"
        placeholder="Meklēt pēc sensora nosaukuma"
      />
    </div>
    
    <!-- Select for Metrics -->
    <div>
      <label for="metric">Meklēt pēc metrikas nosaukuma: </label>
      <select name="metrics" id="metric" @change="handleMetricChange">
        <option value="all">Visas</option>
        <option v-for="metric in showMetrics" :key="metric.id" :value="metric.id">{{ metric.name }}</option>
      </select>
    </div>
    
    <!-- Select for Types -->
    <div>
      <label for="types">Meklēt pēc sensora tipa nosaukuma: </label>
      <select name="types" id="types" @change="handleTypeChange">
        <option value="all">Visi</option>
        <option v-for="type in showTypes" :key="type.id" :value="type.name">{{ type.name }}</option>
      </select>
    </div>
    
    <!-- Table Display -->
    <table>
      <thead>
        <tr>
          <th @click="handleSort('name')">Sensora nosaukums 
            <span v-if="sortColumn === 'name'">{{ sortOrder === 'asc' ? '+' : '-' }}</span>
          </th>
          <th @click="handleSort('typeName')">Sensora tipa nosaukums 
            <span v-if="sortColumn === 'typeName'">{{ sortOrder === 'asc' ? '+' : '-' }}</span>
          </th>
          <th @click="handleSort('timestamp')">Mērījuma laiks(timestamp) 
            <span v-if="sortColumn === 'timestamp'">{{ sortOrder === 'asc' ? '+' : '-' }}</span>
          </th>
          <th @click="handleSort('value')">Mērījuma vērtība 
            <span v-if="sortColumn === 'value'">{{ sortOrder === 'asc' ? '+' : '-' }}</span>
          </th>
          <th @click="handleSort('metricName')">Metrikas nosaukums 
            <span v-if="sortColumn === 'metricName'">{{ sortOrder === 'asc' ? '+' : '-' }}</span>
          </th>
          <th @click="handleSort('unitName')">Mērvienība 
            <span v-if="sortColumn === 'unitName'">{{ sortOrder === 'asc' ? '+' : '-' }}</span>
          </th>
        </tr>
      </thead>
      <tbody>
        <template v-for="sensor in sortedSensors" :key="sensor.id">
          <tr v-for="(metric, metricId) in sensor.metrics" :key="metricId">
            <td>{{ sensor.name }}</td>
            <td>{{ sensor.typeName }}</td>
            <td>{{ new Date(metric.t * 1000).toLocaleString('en-GB').replaceAll('/', '.') }}</td>
            <td>{{ metric.v }}</td>
            <td>{{ metric.name }}</td>
            <td>{{ metric.units.find(unit => unit.selected === true)?.name || 'Unknown' }}</td>
          </tr>
        </template>
      </tbody>
    </table>
  </div>
</template>