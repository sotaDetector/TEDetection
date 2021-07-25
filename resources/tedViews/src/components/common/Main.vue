<template>
  <div class="wrapper">
    <v-head></v-head>
    <v-leftlogo></v-leftlogo>
    <v-sidebar></v-sidebar>
    <div class="content-box">
      <div class="content">
        <transition name="move" mode="out-in">
          <router-view></router-view>
        </transition>
      </div>
    </div>
  </div>
</template>
<script>
import vHead from './Header'
import vLeftlogo from './LeftLogo'
import vSidebar from './SideBar'
export default {
  name: "Main",
  data () {
    return {
    }
  },
  components: {
    vHead, vSidebar, vLeftlogo
  }
}
</script>
<style scoped>
.wrapper {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}
.content-box {
  height: calc(100vh - 40px);
  position: absolute;
  left: 200px;
  right: 0;
  top: 40px;
  bottom: 0;
  overflow-x: auto;
  overflow-y: auto;
  transition: left 0.3s ease-in-out;
  background: #f5f6fa;
}
.content {
  width: auto;
  height: calc(100% - 30px);
  /* min-width: 1024px; */
  min-width: 1000px;
  padding: 15px 15px 20px;
}
</style>