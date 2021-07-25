<template>
  <div class="leftlogo">
    <img src="@/assets/img/logo.png" alt="">
  </div>
</template>
<script>
export default {
  name: "LeftLogo",
  data () {
    return {
    }
  }
}
</script>
<style scoped>
.leftlogo {
  width: 199px;
  /* background: #515a6e; */
  height: 80px;
  position: absolute;
  left: 0;
  top: 0;
  /* border-bottom: 1px solid #515a6e; */
  background: #fff;
}
.leftlogo img {
  width: 166px;
  margin-left: 17px;
  margin-top: 13px;
}
</style>