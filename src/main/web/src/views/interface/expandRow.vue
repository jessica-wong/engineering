<style lang="less">
    @import './advanced-router.less';
</style>

<template>
    <div>
        <Card>
            <Row>
                <Col span="8">
                    <span class="expand-key">参数类型：</span>
                    <span class="expand-value">{{ row.Type }}</span>
                </Col>
            </Row>
            <Table :columns="columnsRequest" :data= row.requestTable></Table>
            <Row >
                <Col span="8">
                    <span class="expand-key">请求参数：</span>
                </Col>
                <Col span="8">
                    <pre class="expand-value">{{row.Schema_request | jsonFormat}}</pre>
                </Col>
            </Row>
            <Table :columns="columnsResponse" :data=row.responseTable ></Table>
            <Row >
                <Col span="8">
                    <span class="expand-key">返回参数：</span>
                </Col>
                <Col span="8">
                    <pre class="expand-value" >{{row.Schema_response | jsonFormat}}</pre>
                    <!--<i-input v-model="formattedJSON" :readonly="true" type="textarea" :autosize="true" placeholder="Enter something..."></i-input>-->
                </Col>
            </Row>
        </Card>

    </div>
</template>
<script>
import Vue from 'vue'
import jsBeautify from 'js-beautify/js/lib/beautify'
import {
  getObjectiveCEntities
} from 'swagger-parser-mock/lib/entity'
    export default {
        props: {
            row: Object
        },
        data(){
            return{
                columnsRequest: [
                    {
                        title: '参数名',
                        key: 'name'
                    },
                    {
                        title: '描述',
                        key: 'describe'
                    },
                    {
                        title: '参数类型',
                        key: 'paramType'
                    },
                    {
                        title: '是否必传',
                        key: 'required'
                    }
                ],
                request:[
                {
                    "name":"test",
                    "description":"description",
                    "paramType":"paramType",
                    "dataType":"1"
                }
                ],
                columnsResponse:[
                    {
                        title: '参数名',
                        key: 'name'
                    },
                    {
                        title: '描述',
                        key: 'describe'
                    },
                    {
                        title: '参数类型',
                        key: 'paramType'
                    },
                ],
                response:[
                {
                    "name":"test",
                    "description":"description",
                    "paramType":"paramType",
                }
                ]
            }
        },
        filters:{
            jsonFormat(value){
                return jsBeautify.js_beautify(value,{indent_size:2})
            }
        }
    };
</script>