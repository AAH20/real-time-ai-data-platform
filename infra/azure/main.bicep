targetScope = 'resourceGroup'

@description('Short lowercase suffix used in globally unique resource names.')
param suffix string

@description('Azure region for the evidence plane.')
param location string = resourceGroup().location

@description('Deploy Event Hubs only for a live streaming demonstration. Disabled by default to control cost.')
param deployStreaming bool = false

param tags object = {
  workload: 'real-time-ai-data-platform'
  evidence: 'synthetic-demo'
  managedBy: 'bicep'
}

resource workspace 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: 'law-realtimeiq-${suffix}'
  location: location
  tags: tags
  properties: {
    retentionInDays: 30
    sku: { name: 'PerGB2018' }
  }
}

resource insights 'Microsoft.Insights/components@2020-02-02' = {
  name: 'appi-realtimeiq-${suffix}'
  location: location
  kind: 'web'
  tags: tags
  properties: {
    Application_Type: 'web'
    WorkspaceResourceId: workspace.id
  }
}

resource storage 'Microsoft.Storage/storageAccounts@2023-05-01' = {
  name: 'strealtimeiq${suffix}'
  location: location
  tags: tags
  sku: { name: 'Standard_LRS' }
  kind: 'StorageV2'
  properties: {
    allowBlobPublicAccess: false
    minimumTlsVersion: 'TLS1_2'
    supportsHttpsTrafficOnly: true
  }
}

resource eventHubs 'Microsoft.EventHub/namespaces@2024-01-01' = if (deployStreaming) {
  name: 'evhns-realtimeiq-${suffix}'
  location: location
  tags: tags
  sku: {
    name: 'Standard'
    tier: 'Standard'
    capacity: 1
  }
  properties: {
    isAutoInflateEnabled: false
    publicNetworkAccess: 'Enabled'
    minimumTlsVersion: '1.2'
  }
}

resource orderEvents 'Microsoft.EventHub/namespaces/eventhubs@2024-01-01' = if (deployStreaming) {
  parent: eventHubs
  name: 'order-risk-events'
  properties: {
    messageRetentionInDays: 1
    partitionCount: 2
  }
}

output applicationInsightsId string = insights.id
output evidenceStorageId string = storage.id
output streamingEnabled bool = deployStreaming
