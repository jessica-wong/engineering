<style lang="less">
    @import '../../styles/common.less';
    @import './advanced-router.less';
</style>

<template>
    <div>
        <Row type="flex" class="height-100">
            <Col span="8">
                <!--<i-button type="success" @click="addInterface" style="margin-top-10">新建接口</i-button>-->
                <i-button type="success" @click="synchronizeWebApi">同步接口</i-button>
            </Col>
            <Col span='8'>
                <Input v-model="searchValue" placeholder="接口path，如/api/swaggerservice/createwebapis">
                    <Button slot="append" icon="ios-search"  @click="searchApiByPath"></Button>
                </Input>
            </Col>
        </Row>
        <Row class="margin-top-10">
            <Card>
                <div class="margin-top-10">
                    <Table :columns="listColumns" :data="list"></Table>
                </div>
            </Card>
        </Row>
        <Modal
            v-model="modalAddTag"
            title="为接口添加标签"
            @on-ok="addWebApiTag"
            @on-cancel="cancel">
            <Select v-model="tagSelected" @on-change="handleSelectTag" placeholder="请选择标签，可为空">
                <Option v-for="item in tagList" :value="item.tag_id_name" :key="item.value">{{ item.tag_id_name }}</Option>
            </Select>
        </Modal>
    </div>

</template>

<script>
import expandRow from './expandRow.vue';
import axios  from 'axios';
export default {
    components: {
        expandRow
    },
    data () {
        return {
            listColumns: [
                {
                    type: 'expand',
                    width: 50,
                    render: (h, params) => {
                        return h(expandRow, {
                            props: {
                                row: params.row
                            }
                        });
                    }
                },
                {
                    type: 'selection',
                    width: 60,
                    align: 'center'
                },
                {
                    title: '请求方式',
                    key: 'Method',
                    filters: [
                            {
                                label: 'get',
                                value: 'get'
                            },
                            {
                                label: 'post',
                                value: 'post'
                            }
                        ],

                    filterMethod (value, row) {
                        return row.Method.indexOf(value) > -1
                    },

                },
                {
                    title: '接口地址',
                    key: 'Path'
                },
                {
                     title: '接口描述',
                     key: 'Summary'
                },
                {
                    title: '接口状态',
                    key: 'DiffTypeName',
                    filters: [
                        {
                            label: '新增接口',
                            value: '新增接口'
                        },
                        {
                            label: '编辑接口',
                            value: '编辑接口'
                        },
                        {
                            label: '删除接口',
                            value: '删除接口'
                        },
                    ],
                    filterMethod (value, row) {
                        return row.DiffTypeName.indexOf(value) > -1
                    },
                },
                {
                    title: '操作',
                    key: 'action',
//                    width: 300,
                    align: 'center',
                    render: (h, params) => {
                        return h('div', [
                            h('Button', {
                                props: {
                                    type: 'primary',
                                    size: 'small'
                                },
                                style: {
                                    marginRight: '5px'
                                },
                                on: {
                                    click: () => {
                                        this.tagData.OperationId=params.row.OperationId
                                        this.modalAddTag = true
                                    }
                                }
                            }, '添加标签'),
//                            h('Button', {
//                                props: {
//                                    type: 'error',
//                                    size: 'small'
//                                },
//                                on: {
//                                    click: () => {
//                                        this.removeInterfaceData.interfaceId = params.row.Id
//                                        this.removeInterface()
//                                    }
//                                }
//                            }, '确认变更')
                        ]);
                    }
                }
            ],
            list: [],
            searchValue:"",
            formItem:{},
            modalAddTag:false,
            tagList:[],
            tagSelected:[],
            tagData:{
                OperationId:"",
                tagId:"",
                projectId:"",
                applicationId:""
            },
        };
    },
    methods: {
        addInterface(){
            this.$router.push({path:"/interface/interface-edit",query:{projectId:this.$route.query.projectId,applicationId:this.$route.query.applicationId}})
        },
        getWebapiList(){
            axios.get("/v1/webapi/getWebApiList",
            {params:{projectId:this.$route.query.projectId,applicationId:this.$route.query.applicationId}}
                ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    var deffType={
                        1:"新增接口",
                        2:"编辑接口",
                        3:"删除接口",
                    }
                    this.list = res.data.message.map(one=>{
                        one.DiffTypeName = deffType[one.DiffType];
                        return one;
                    });
                }else{
                    this.$Message.error("获取数据失败");
                }
            }
            )
        },
        searchApiByPath(){
            let Path=this.searchValue
            axios.get("/v1/webapi/getWebApiInfoByPath",{params:{projectId:this.$route.query.projectId,applicationId:this.$route.query.applicationId,Path:Path}}
                ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.list = []
                    this.list = res.data.message;
                }else{
                    this.$Message.error("获取数据失败");
                }
            }
            )
        },
        synchronizeWebApi(){
            return axios.get("/v1/application/getVersionConfig",{params:{projectId:this.$route.query.projectId,applicationId:this.$route.query.applicationId}}).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.formItem = res.data.message[0];
                    axios.get("/v1/webapi/synchronizeWebApi",{params:{projectId:this.$route.query.projectId,applicationId:this.$route.query.applicationId,swaggerJsonOrUrl:this.formItem.swagger_url}}
                        ).then((res)=>{
                        console.log(res)
                        if(res.data.success){
                            this.$Message.success("同步成功");
                        }else{
                            this.$Message.error("同步失败");
                        }
                    })
                }else{
                    this.$Message.error("获取数据失败")
                }
            })
        },
        handleSelectAll (status) {
            this.$refs.selection.selectAll(status);
        },
        getWebApiTag(index){
            axios.get("/v1/tag/getTagsForApi"
            ).then((res)=>{
                //console.log(res)
                if(res.data.success){
//                      this.$Message.success("成功")
                      var tag_id_name_Enum={
                          1:"新增",
                          2:"编辑",
                          3:"删除",
                      }
                      this.tagList = res.data.message.map(one=>{
                          one.tag_id_name = tag_id_name_Enum[one.id];
                          return one;
                      });

                }else{
                    this.$Message.error("失败")
                }
            }
            )
        },
        handleSelectTag () {
            if (this.tagSelected=="新增"){
                return localStorage.tagsList = 1;
            }else if (this.tagSelected=="编辑"){
                return localStorage.tagsList = 2;
            }else{
                return localStorage.tagsList = 3;
            }
        },
        addWebApiTag(){
            this.tagData.projectId=this.$route.query.projectId
            this.tagData.applicationId=this.$route.query.applicationId
            this.tagData.tagId = this.handleSelectTag()
//            axios.post("/v1/tag/addWebApiTag",this.tagData
            axios.post("/v1/webapi/setWebApiDiff",this.tagData
                ).then((res)=>{
                console.log(res)
                if(res.data.success){
                    this.$Message.success("添加标签成功");
                }else{
                    this.$Message.error("添加标签失败");
                }
            })
        },
        cancel () {
            this.$Message.info('Clicked cancel');
        },
    },
    created () {
        this.getWebapiList();
        this.getWebApiTag();
    }
};
</script>
