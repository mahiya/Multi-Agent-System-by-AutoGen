#!/bin/bash -e

# デプロイ設定
REGION='japaneast'
RESOURCE_GROUP="aoai-demo-apps"
APP_PLAN_NAME="aoai-demo-apps-plan"
APP_NAME_POSTFIX=$(az account show --query "id" --output tsv)
APP_NAME="multi-agent-"${APP_NAME_POSTFIX:0:8}
SKU='B3'

# App Service プランを作成
az appservice plan create \
    --name $APP_PLAN_NAME \
    --resource-group $RESOURCE_GROUP \
    --sku $SKU \
    --is-linux \
    --location $REGION

# Azure Web App を作成
az webapp create \
    --name $APP_NAME \
    --plan $APP_PLAN_NAME \
    --resource-group $RESOURCE_GROUP \
    --runtime 'PYTHON:3.11'

# Azure Web Apps の環境変数を設定
az webapp config appsettings set \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --settings "SCM_DO_BUILD_DURING_DEPLOYMENT"="true" \
               "DEPLOYMENT_NAME=$DEPLOYMENT_NAME" \
               "API_KEY=$API_KEY" \
               "API_ENDPOINT=$API_ENDPOINT" \
               "API_VERSION=$API_VERSION"

# スタートアップコマンドを設定
az webapp config set \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --startup-file "python -m streamlit run src/app.py --server.port 8000 --server.address 0.0.0.0"

# アプリケーションをデプロイ
az webapp up \
    --resource-group $RESOURCE_GROUP \
    --name $APP_NAME \
    --plan $APP_PLAN_NAME \
    --sku $SKU \
    --location $REGION \
    --runtime 'PYTHON:3.11'
