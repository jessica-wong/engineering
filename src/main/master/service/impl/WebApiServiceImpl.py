# -*- coding: utf-8 -*-

import json
import traceback
from src.main.master.common.constants import SystemConfig
from src.main.master.util.logUtil.log import Log
from src.main.master.entity.DataResult import DataResult
from src.main.master.dao.WebApiDao import WebApiDaoInterface
from src.main.master.core.AdminDecorator import AdminDecoratorServer

#set log
logger = Log('WebApiServiceImpl')
logger.write_to_file(SystemConfig.logPathPrefix+"WebApiServiceImpl.log")

class WebApiService(object):

    def __init__(self):
        self.WebApiDaoInterface = WebApiDaoInterface()

    @AdminDecoratorServer.execImplDecorator()
    def addWebApi(self,args):
        if "params" not in args:
            args.setdefault("params",None)
        else:
            params=json.dumps(args.get("params"))
            args.pop("params")
            args.setdefault("params",params)
        if "failure_response" not in args:
            args.setdefault("failure_response",None)
        else:
            failure_response=json.dumps(args.get("failure_response"))
            args.pop("failure_response")
            args.setdefault("failure_response",failure_response)
        if "success_response" not in args:
            args.setdefault("success_response",None)
        else:
            success_response=json.dumps(args.get("success_response"))
            args.pop("success_response")
            args.setdefault("success_response",success_response)
        if "response_type" not in args:
            args.setdefault("response_type",None)
        if "status" not in args:
            args.setdefault("status",None)
        if "remarks" not in args:
            args.setdefault("remarks",None)
        # logger.error(args.get("params"))
        # logger.error(type(args.get("success_response")))
        args.setdefault("create_username","jessica")
        return self.WebApiDaoInterface.addWebApi(args)

    @AdminDecoratorServer.execImplDecorator()
    def getWebApiForVersion(self,applicationId,projectId):
        args={}
        args.setdefault("applicationId",applicationId)
        args.setdefault("projectId", projectId)
        return self.WebApiDaoInterface.getWebApiForVersion(args)

    @AdminDecoratorServer.execImplDecorator()
    def deleteWebApi(self,args):
        return self.WebApiDaoInterface.deleteWebApi(args)

    @AdminDecoratorServer.execImplDecorator()
    def updateWebApi(self,args):
        if "params" not in args:
            args.setdefault("params",None)
        else:
            params=json.dumps(args.get("params"))
            args.pop("params")
            args.setdefault("params",params)
        if "failure_response" not in args:
            args.setdefault("failure_response",None)
        else:
            failure_response=json.dumps(args.get("failure_response"))
            args.pop("failure_response")
            args.setdefault("failure_response",failure_response)
        if "success_response" not in args:
            args.setdefault("success_response",None)
        else:
            success_response=json.dumps(args.get("success_response"))
            args.pop("success_response")
            args.setdefault("success_response",success_response)
        dataResult = self.WebApiDaoInterface.getWebApiInfoById(args)
        # logger.error(dataResult.__dict__)
        if dataResult.getSuccess() and len(dataResult.getMessage()) > 0:
            for key,value in dataResult.getMessage()[0].items():
                if key not in args:
                    args.setdefault(key,value)
            return self.WebApiDaoInterface.updateWebApi(args)
        logger.error("interfaceId [{}] is invalid".format(args.get("interfaceId")))
        dataResult.setMessage("interfaceId [{}] is invalid".format(args.get("interfaceId")))
        return dataResult

    def getWebApiInfoById(self,webApiId):
        args = {}
        args.setdefault("webApiId", webApiId)
        return self.WebApiDaoInterface.getWebApiForVersion(args)

    def getWebApiList(self,applicationId,projectId):
        webApiResult = DataResult()
        webApi=[]
        args = {}
        args.setdefault("applicationId", applicationId)
        args.setdefault("projectId", projectId)
        dataResult = self.WebApiDaoInterface.getWebApiList(args)
        if dataResult.getSuccess():
            for item in dataResult.getMessage():
                data={}
                data["Id"]=item["Id"]
                data["Method"]=item["Method"]
                data["OperationId"]=item["OperationId"]
                data["Path"]=item["Path"]
                data["Produces"]=item["Produces"]
                data["Summary"]=item["Summary"]
                data["DiffType"] = item["DiffType"]
                Id={"Id":item["Id"]}
                # data["Type"]="query"
                data_request=self.WebApiDaoInterface.getWebApiRequest(Id)
                if data_request.getSuccess():
                    data["Schema_request"] = []
                    data["requestTable"] = []
                    if len(data_request.getMessage())>0:
                        if data_request.getMessage()[0]["In"]=="query":
                            for res in data_request.getMessage():
                                if 'currentUser' in res["Name"]:
                                    continue
                                else:
                                    data["Type"] = "query"
                                    # tmpJson ={}
                                    # tmpJson["name"]=res["Name"]
                                    # tmpJson["defaultValue"] =res["Schema"]
                                    # tmpJson["describe"] = res["Description"]
                                    # data["Schema_request"].append(tmpJson)
                                    data["Schema_request"]={}
                                    webapiParameterId={"webapiParameterId":res["Id"]}
                                    dataResultProperty=self.WebApiDaoInterface.getParameterProperty(webapiParameterId)
                                    if dataResultProperty.getSuccess() and len(dataResultProperty.getMessage())>0:
                                        requestJson={}
                                        resProperty = dataResultProperty.getMessage()
                                        requestJson["name"] = res["Name"]
                                        requestJson["describe"] = resProperty[0]["Description"]
                                        requestJson["paramType"] = resProperty[0]["Type"]
                                        requestJson["required"] = resProperty[0]["Required"]
                                        data["requestTable"].append(requestJson)
                        else:
                            data["Type"] = "body"
                            data["Schema_request"] = data_request.getMessage()[0]["Schema"]
                            webapiParameterId = {"webapiParameterId": data_request.getMessage()[0]["Id"]}
                            dataResultProperty = self.WebApiDaoInterface.getParameterProperty(webapiParameterId)
                            if dataResultProperty.getSuccess() and len(dataResultProperty.getMessage())>0:
                                for requset in dataResultProperty.getMessage():
                                    requestJson = {}
                                    requestJson["name"] = requset["Name"]
                                    requestJson["describe"] = requset["Description"]
                                    requestJson["paramType"] = requset["Type"]
                                    requestJson["required"] = requset["Required"]
                                    data["requestTable"].append(requestJson)
                            else:
                                data["requestTable"]=[]
                    else:
                        data["Type"] = ""
                        data["Schema_request"] = []
                        data["requestTable"] = []
                    logger.info(data["Schema_request"])
                data_response=self.WebApiDaoInterface.getWebApiResponse(Id)
                if data_response.getSuccess():
                    data["Schema_response"]=data_response.getMessage()[0]["Schema"]
                    data["responseTable"] = []
                    webapiResponseId = {"webapiParameterId": data_response.getMessage()[0]["Id"]}
                    dataResponseProperty = self.WebApiDaoInterface.getParameterProperty(webapiResponseId)
                    if dataResponseProperty.getSuccess() and len(dataResponseProperty.getMessage())>0:
                        for response in dataResponseProperty.getMessage():
                            responseJson = {}
                            responseJson["name"] = response["Name"]
                            responseJson["describe"] = response["Description"]
                            responseJson["paramType"] = response["Type"]
                            data["responseTable"].append(responseJson)
                    else:
                        data["responseTable"]=[]
                    logger.info(data["Schema_response"])
                webApi.append(data)
            webApiResult.setMessage(webApi)
            webApiResult.setSuccess(True)
        return webApiResult

    def getWebApiInfoByPath(self,applicationId,projectId,Path):
        args = {}
        args.setdefault("Path", Path)
        args.setdefault("applicationId", applicationId)
        args.setdefault("projectId", projectId)
        return self.WebApiDaoInterface.getWebApiInfoByPath(args)

    # 获取无参数接口用,暂时未用service，仅用dao
    def getWebApiPathForProject(self, projectId, applicationId):
        args = {}
        args.setdefault("applicationId", applicationId)
        args.setdefault("projectId", projectId)
        logger.info(args)
        return self.WebApiDaoInterface.getWebApiPathForProject(args)

    # 根据path获取接口详细信息用于自动生成用例 暂时未用service，仅用dao
    def getWebApiInfosForCase(self, projectId, applicationId,path):
        args = {}
        args.setdefault("applicationId", applicationId)
        args.setdefault("projectId", projectId)
        args.setdefault("path", path)
        logger.info(args)
        return self.WebApiDaoInterface.getWebApiInfosForCase(args)

    def setWebApiDiff(self,args):
        return self.WebApiDaoInterface.setWebApiDiff(args)