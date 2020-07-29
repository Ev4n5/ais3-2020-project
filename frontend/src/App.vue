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
    },
    relationships: {
      INTERACTS: {
        thickness: "weight",
        caption: false,
      },
      [NeoVis.NEOVIS_DEFAULT_CONFIG]: {
        thickness: "defaultThicknessProperty",
        caption: "defaultCaption",
      },
    },
    initial_cypher:
      'MATCH p=(bacon:Person {name:"Kevin Bacon"})-[*1..4]-(hollywood) RETURN p',
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
