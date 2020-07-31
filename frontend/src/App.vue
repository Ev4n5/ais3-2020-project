<template>
  <div id="app" class="container-fluid">
    <!-- <img alt="Vue logo" src="./assets/logo.png" /> -->
    <!-- <HelloWorld msg="Welcome to Your Vue.js App" /> -->
    <div class="row text-left">
      <div class="col-md-2 my-4">
        <h4 class="text-center">圖示</h4>
        <ul class="list-group">
          <li class="list-group-item">
            <font-awesome-icon :icon="['fas', 'circle']" style="color:purple" /> tcp
          </li>
          <li class="list-group-item">
            <font-awesome-icon :icon="['fas', 'circle']" style="color:red" /> udp
          </li>
          <li class="list-group-item">
            <font-awesome-icon :icon="['fas', 'circle']" style="color:orange" /> arp
          </li>
          <li class="list-group-item">
            <font-awesome-icon :icon="['fas', 'circle']" style="color:green" /> icmp
          </li>
        </ul>
      </div>
      <div class="col-md-10">
        <h1 class="my-4 text-center">OT 設備流量視覺化</h1>
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
                  <button class="btn btn-secondary" v-on:click="myClick">重整</button>
                </div>
              </div>
              <div id="viz2" class="neovis-container"></div>
            </div>
          </div>
        </div>
        <!-- <div class="card">
          <div class="card-body">This is some text within a card body.</div>
        </div> -->
        <!-- <div class="input-group">
      <flat-pickr v-model="date" :config="config"></flat-pickr>
      <button class="btn btn-default" type="button" title="Toggle" data-toggle>
        <font-awesome-icon :icon="['far', 'calendar-alt']" />
      </button>
        </div>-->
      </div>
    </div>
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
      caption: (node) => {
        return node.properties.mac.substr(-5);
      },
      community: "community",
    },
  },
  relationships: {
    INTERACTS: {
      thickness: "weight",
      caption: false,
    },
    [NeoVis.NEOVIS_DEFAULT_CONFIG]: {
      // thickness: "defaultThicknessProperty",
      caption: "defaultCaption",
      thickness: "count",
    },
    tcp: {
      color: "purple",
    },
    udp: {
      color: "red",
    },
    arp: {
      color: "orange",
    },
    icmp: {
      color: "green",
    },
  },
};

const mac_prefix = "02:42:ac:11";
let viz = null;
const vizInit = (y1, mon1, d1, h1, min1, y2, mon2, d2, h2, min2) => {
  console.log("vizInit");
  let config = {
    ...vizConfig,
    container_id: "viz",
    initial_cypher:
      `MATCH (a:Host)-[r]->(b)
WHERE r.created_at > datetime({year: ${y1}, month: ${mon1}, day: ${d1}, hour: ${h1}, minute: ${min1}, timezone: "+08:00"})
AND r.created_at < datetime({year: ${y2}, month: ${mon2}, day: ${d2}, hour: ${h2}, minute: ${min2}, timezone: "+08:00"})
AND a.mac STARTS WITH '${mac_prefix}'
AND b.mac STARTS WITH '${mac_prefix}'
WITH a, collect(r) AS r, b, count(r) as cnt, type(r) AS relName
RETURN a, b, apoc.create.vRelationship(a, relName, {type: relName, count: cnt}, b) as rel`,
  };

  viz = new NeoVis.default(config);
  viz.render();
};

let viz2 = null;
const vizInit2 = () => {
  console.log("vizInit2");
  let config = {
    ...vizConfig,
    container_id: "viz2",
    initial_cypher:
      `WITH datetime({timezone:"+08:00"}) AS cur
MATCH (a:Host)-[r]->(b)
WHERE r.created_at > datetime({epochSeconds: cur.epochSeconds - 60*3})
AND a.mac STARTS WITH '${mac_prefix}'
AND b.mac STARTS WITH '${mac_prefix}'
WITH a, collect(r) AS r, b, count(r) as cnt, type(r) AS relName
RETURN a, b, apoc.create.vRelationship(a, relName, {type: relName, count: cnt}, b) as rel`,
  };

  viz2 = new NeoVis.default(config);
  viz2.render();
};

const myClick = () => {
  console.log("reload");
  viz2.reload();
};

export default {
  name: "App",
  data: () => ({
    dateFrom: "2020-07-29 12:00",
    dateTo: "2020-07-31 15:00",
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
      vizInit(
        ...val.split(/[- :]/).map((e) => parseInt(e)),
        ...this.dateTo.split(/[- :]/).map((e) => parseInt(e))
      );
    },
    dateTo(val) {
      vizInit(
        ...this.dateFrom.split(/[- :]/).map((e) => parseInt(e)),
        ...val.split(/[- :]/).map((e) => parseInt(e))
      );
    },
  },
  methods: {
    myClick: myClick,
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
  height: 600px;
}
</style>
