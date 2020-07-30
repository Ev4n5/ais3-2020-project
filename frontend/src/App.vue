<template>
  <div id="app">
    <img alt="Vue logo" src="./assets/logo.png" />
    <!-- <HelloWorld msg="Welcome to Your Vue.js App" /> -->
    <div id="viz"></div>
  </div>
</template>

<script>
// import HelloWorld from "./components/HelloWorld.vue";
const NeoVis = window.NeoVis;

let viz = null;
const vizInit = () => {
  console.log("vizInit");
  var config = {
    container_id: "viz",
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
    initial_cypher:
      // 'MATCH p=(bacon:Person {name:"Kevin Bacon"})-[*1..4]-(hollywood) RETURN p',
      `MATCH (a:Host)-[r]->(b)
WHERE r.created_at < datetime({year: 2020, month: 8, day: 30, hour: 17, minute: 10, second: 0, timezone: "+08:00"})
WITH a, collect(r) AS r, b, count(r) as cnt, type(r) AS relName
RETURN a, b, apoc.create.vRelationship(a, relName, {count: cnt}, b) as rel`,
  };

  viz = new NeoVis.default(config);
  viz.render();
};
export default {
  name: "App",
  components: {
    // HelloWorld,
  },
  mounted: () => {
    vizInit();
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
  margin-top: 60px;
}

#viz {
  height: 600px;
}
</style>
