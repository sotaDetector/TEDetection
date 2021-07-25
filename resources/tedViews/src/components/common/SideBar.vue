<template>
  <div class="sidebar">
    <Row>
      <Col span="4">
      <Menu :theme="theme2" accordion width="200px" :active-name="actName" ref="side_menu" :open-names="openItem">
        <div v-for="info in menuList" :key="info.menuId">
          <Submenu v-if="info.children && info.children.length>0" :name="info.menuId">
            <template slot="title">
              <Icon class="menu_icon" :type="info.ico" :size="20" :key="'ico' + info.menuName" style="color:#8c0776" />
              <!-- <img class="menuicon" :src="info.ico" alt=""> -->
              {{info.menuName}}
            </template>
            <MenuItem :name="item.url" :to="{ path: '/' +item.url}" v-for="item in info.children" :key="item.menuId" ref="menu_item">
            <Icon class="menu_icon" :type="item.ico" :size="20" :key="'ico' + item.menuName" style="color:#8c0776" />{{item.menuName}}</MenuItem>
          </Submenu>

          <MenuItem v-else :name="info.url" :to="{ path: '/' + info.url }" ref="menu_item">
          <!-- <img class="menuicon" :src="info.ico" /> -->
          <Icon class="menu_icon" :type="info.ico" :size="10" :key="'ico' + info.menuName" style="color:#8c0776" />
          {{info.menuName}}
          </MenuItem>
        </div>
      </Menu>
      </Col>
    </Row>
  </div>
</template>

<script>
// import { currentUserInfoMethod } from 'network/login'
import { menuList } from '@/utils/menu.js'
export default {
  name: "SideBar",
  data () {
    return {
      theme2: 'light',
      menuList,
      actName: '',
      openItem: []
    }
  },
  watch: {
    '$route.name': {
      handler (n) {
        // var actName = n == 'morningExamDetail' ? 'morningExamManage' : n == 'ops/morningExamDetail' ? 'ops/morningExamManage' : n
        var actName = n.slice(0,1).toLowerCase() + n.slice(1)
        var findItem = this.menuList.find(i => i.children && i.children.find(j => j.url == actName))
        if(findItem) {
          this.openItem = []
          this.openItem.push(findItem.menuId)
        }
        this.actName = actName
        this.$nextTick(() => {
          this.$refs.side_menu.updateOpened()
          this.$refs.side_menu.updateActiveName()
        })
      },
      immediate: true,
      deep: true
    }
  },
  created () {
    // 刷新当前的用户信息
    // currentUserInfoMethod(this.$store.state.token).then(data => {
    //   if(data.rs === 1) {
    //     // console.log(data)
    //     // console.log(this.$route);
    //     this.menuList = data.menuList
    //     // 刷新之后将当前用户信息放到store中去
    //     this.$store.commit('refreshCurrentUserInfo',
    //       {
    //         token: data._token_iben,
    //         menuList: data.menuList,
    //         requestPaths: data.requestPaths,
    //         userName: data.currentUserInfo.userName
    //       });
    //     this.$nextTick(() => {
    //       this.openMenu();
    //     });
    //   } else {
    //     this.$Message.error(data.data.errorMsg)
    //   }
    // })
  },
  methods: {
    openMenu (curName) {
      if(!curName) {
        curName = this.$route.path;
      }
      let ref = this.$refs.menu_item;
      console.log(typeof (this.$refs));
      console.log(this.$refs)
      if(!ref) {
        console.log("菜单未渲染完成")
        return;
      }
      for(let i = 0; i < ref.length; i++) {
        // MenuItem 处于选中状态就展开 Submenu
        // console.log(ref[i].name,curName)
        if("/" + ref[i].name == curName) {
          ref[i].$parent.opened = true;
          ref[i].active = true;
          if(ref[i].$parent.$parent) {
            ref[i].$parent.$parent.opened = true;
            ref[i].$parent.active = true;
          }
        }
      }
      // console.log(new Date() + "当前路由：" + curName + "---" + Math.floor(Math.random()*10))
    }
  },
  mounted () {
    this.$nextTick(() => {
      this.$refs.side_menu.updateOpened()
      this.$refs.side_menu.updateActiveName()
    })
  }
}
</script>
<style scoped>
.sidebar {
  position: absolute;
  left: 0;
  top: 110px;
  bottom: 0;
  z-index: 9;
  height: 100%;
  /* background: #515a6e; */
}
.menuicon {
  width: 18px;
  vertical-align: middle;
  margin-right: 4px;
  margin-top: -1px;
}
.menu_icon {
  vertical-align: middle;
  margin-right: 7px;
}
</style>
