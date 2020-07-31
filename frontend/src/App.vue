<template>
  <div id="app" class="container-fluid">
    <!-- <img alt="Vue logo" src="./assets/logo.png" /> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App" /> -->
    <h1 class="my-4">OT 設備流量視覺化</h1>
    <div class="row bd-highlight mb-3">
      <div class="col-md my-1">
        <div class="card">
          <div class="card-header">
            <div class="row">
              <h2 class="col-md-8 text-left">正常流量</h2>
              <!-- <font-awesome-icon :icon="['fas', 'caret-down']" class="float-right" /> -->
              <div class="dropdown float-right my-0 col-md-4">
                <button
                  class="btn btn-secondary dropdown-toggle float-right"
                  type="button"
                  id="dropdownMenuButton"
                  data-toggle="dropdown"
                  aria-haspopup="true"
                  aria-expanded="false"
                >設定</button>
                <div class="dropdown-menu" aria-labelledby="dropdownMenuButton">
                  <a class="dropdown-item" href="#">
                    from:
                    <flat-pickr
                      v-model="dateFrom"
                      :config="config"
                      class="form-control"
                      placeholder="Select date"
                      name="date"
                    ></flat-pickr>
                  </a>
                  <a class="dropdown-item" href="#">
                    to:
                    <flat-pickr
                      v-model="dateTo"
                      :config="config"
                      class="form-control"
                      placeholder="Select date"
                      name="date"
                    ></flat-pickr>
                  </a>
                </div>
              </div>
            </div>
          </div>
          <div id="viz" class="neovis-container"></div>
        </div>
      </div>
      <div class="col-md my-1">
        <div class="card">
          <div class="card-header">
            <div class="row">
              <h2 class="col-md text-left">目前流量</h2>
            </div>
          </div>
          <div id="viz2" class="neovis-container"></div>
        </div>
      </div>
    </div>
    <!-- <div class="input-group">
      <flat-pickr v-model="date" :config="config"></flat-pickr>
      <button class="btn btn-default" type="button" title="Toggle" data-toggle>
        <font-awesome-icon :icon="['far', 'calendar-alt']" />
      </button>
    </div>-->
  </div>
</template>

<script>
// import HelloWorld from "./components/HelloWorld.vue";
const NeoVis = window.NeoVis;
import flatPickr from "vue-flatpickr-component";
import "flatpickr/dist/flatpickr.css";
const vizConfig = {
  server_url: "bolt://localhost:7687",
  server_user: "neo4j",
  server_password: "neo4jneo4j",
  labels: {
    Character: {
      caption: "name",
      size: "pagerank",
      community: "community",
      title_properties: ["name", "pagerank"],
    },
    [NeoVis.NEOVIS_DEFAULT_CONFIG]: {
      caption: "defaultCaptionProperty",
      size: "defaultPagerank",
      community: "defaultCommunity",
    },
    Host: {
      caption: "mac",
    },
  },
  relationships: {
    INTERACTS: {
      thickness: "weight",
      caption: false,
    },
    [NeoVis.NEOVIS_DEFAULT_CONFIG]: {
      // thickness: "defaultThicknessProperty",
      // caption: "defaultCaption",
      thickness: "count",
      caption: true,
    },
    tcp: {
      color: "purple",
      thickness: "count",
    },
    udp: {
      color: "red",
      thickness: "count",
    },
  },
};

let viz = null;
const vizInit = (y1, mon1, d1, h1, min1, y2, mon2, d2, h2, min2) => {
  console.log("vizInit");
  let config = {
    ...vizConfig,
    container_id: "viz",
    initial_cypher:
      // 'MATCH p=(bacon:Person {name:"Kevin Bacon"})-[*1..4]-(hollywood) RETURN p',
      `MATCH (a:Host)-[r]->(b)
WHERE r.created_at > datetime({year: ${y1}, month: ${mon1}, day: ${d1}, hour: ${h1}, minute: ${min1}, timezone: "+08:00"})
AND r.created_at < datetime({year: ${y2}, month: ${mon2}, day: ${d2}, hour: ${h2}, minute: ${min2}, timezone: "+08:00"})
WITH a, collect(r) AS r, b, count(r) as cnt, type(r) AS relName
RETURN a, b, apoc.create.vRelationship(a, relName, {count: cnt}, b) as rel`,
  };

  viz = new NeoVis.default(config);
  viz.render();
};

const vizInit2 = () => {
  console.log("vizInit2");
  let config = {
    ...vizConfig,
    container_id: "viz2",
    initial_cypher:
      // 'MATCH p=(bacon:Person {name:"Kevin Bacon"})-[*1..4]-(hollywood) RETURN p',
      `MATCH (a:Host)-[r]->(b)
WHERE r.created_at > datetime({year: 2020, month: 7, day: 30, hour: 0, minute: 0, timezone: "+08:00"})
WITH a, collect(r) AS r, b, count(r) as cnt, type(r) AS relName
RETURN a, b, apoc.create.vRelationship(a, relName, {count: cnt}, b) as rel`,
  };

  viz = new NeoVis.default(config);
  viz.render();
};

export default {
  name: "App",
  data: () => ({
    dateFrom: "2020-07-29 12:00",
    dateTo: "2020-07-31 12:00",
    date: null,
    config: {
      wrap: true,
      enableTime: true,
    },
  }),
  components: {
    // HelloWorld,
    flatPickr,
  },
  mounted() {
    const from = this.dateFrom.split(/[- :]/);
    const to = this.dateTo.split(/[- :]/);
    vizInit(...from, ...to);
    vizInit2();
  },
  watch: {
    dateFrom(val) {
      vizInit(...val.split(/[- :]/), ...this.dateTo.split(/[- :]/));
    },
    dateTo(val) {
      vizInit(...this.dateFrom.split(/[- :]/), ...val.split(/[- :]/));
    },
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  /* margin-top: 60px; */
}

.neovis-container {
  height: 400px;
}
</style>
