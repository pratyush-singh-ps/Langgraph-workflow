# External APIs Package

A comprehensive package for integrating with external APIs including CCP VAP, CCP Execute, Databricks, and database operations.

## 📁 Package Structure

```
external_apis/
├── __init__.py              # Package initialization
├── config.py                # Configuration management
├── models.py                # Pydantic models
├── ccp_vap_client.py        # CCP VAP API client
├── ccp_execute_client.py    # CCP Execute API client
├── databricks_client.py     # Databricks API client
├── database_client.py       # Database operations client
├── generic_client.py        # Generic HTTP client
├── routes.py                # FastAPI routes
└── README.md                # This file
```

## 🚀 Features

- **CCP VAP Integration**: Graph entities and link status
- **CCP Execute Integration**: Execution details
- **Databricks Integration**: NCS service principal status
- **Database Operations**: PostgreSQL query execution
- **Generic HTTP Client**: Any GET request to any endpoint
- **Async Support**: All operations are async for better performance
- **Error Handling**: Comprehensive error handling and retries
- **Type Safety**: Full Pydantic model validation

## 📋 API Endpoints

### CCP VAP Endpoints

#### GET `/external/getGraphEntity`
Get graph entities from CCP VAP.

**Query Parameters:**
- `branch_name`: Branch name
- `ccp_entity_name`: CCP entity name  
- `project_name`: Project name

**Example:**
```bash
curl "http://localhost:8000/external/getGraphEntity?branch_name=master&ccp_entity_name=abc&project_name=custom_ams_cubes"
```

#### GET `/external/getLinkStatus/{project_id}`
Get link status from CCP VAP.

**Path Parameters:**
- `project_id`: Project ID

**Example:**
```bash
curl "http://localhost:8000/external/getLinkStatus/123"
```

### CCP Execute Endpoints

#### GET `/external/getExecutionDetails/{execution_id}`
Get execution details from CCP Execute.

**Path Parameters:**
- `execution_id`: Execution ID

**Example:**
```bash
curl "http://localhost:8000/external/getExecutionDetails/10449294"
```

### Databricks Endpoints

#### GET `/external/getClientNCSDetails`
Get client NCS details from Databricks.

**Example:**
```bash
curl "http://localhost:8000/external/getClientNCSDetails"
```

### Database Endpoints

#### POST `/external/executeDBQuery`
Execute database query.

**Request Body:**
```json
{
  "environment": "qa",
  "query": "SELECT * FROM users WHERE id = %s",
  "parameters": ["123"]
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/external/executeDBQuery" \
     -H "Content-Type: application/json" \
     -d '{"environment": "qa", "query": "SELECT * FROM users LIMIT 5"}'
```

### Generic Endpoints

#### POST `/external/getJobRunDetails`
Get job run details from any endpoint.

**Request Body:**
```json
{
  "endpoint": "http://example.com/api/job/123"
}
```

**Example:**
```bash
curl -X POST "http://localhost:8000/external/getJobRunDetails" \
     -H "Content-Type: application/json" \
     -d '{"endpoint": "http://example.com/api/job/123"}'
```

## 🔧 Configuration

### Environment Variables

The package uses the following configuration:

```python
# CCP VAP
CCP_VAP_BASE_URL = "http://ccp-vap.commerceiq.ai"

# CCP Execute  
CCP_EXECUTE_BASE_URL = "http://ccp-execute.commerceiq.ai"

# Databricks
DATABRICKS_BASE_URL = "http://databricks-ncs.beta-dbx.commerceiq.ai"

# Database Secrets
DATABASE_SECRETS = {
    "qa": "rds/beta/ccp-beta-psql",
    "beta": "rds/beta/ccp-beta-psql",
    "prod": "rds/prod/ccp-prod-psql"
}
```

### Database Configuration

The package supports three environments:
- **QA**: `ccp_qa` database
- **Beta**: `ccp_beta` database  
- **Prod**: `ccp_prod` database

## 🛠️ Usage

### Basic Usage

```python
from external_apis import CCPVAPClient, CCPExecuteClient, DatabricksClient

# Initialize clients
vap_client = CCPVAPClient()
execute_client = CCPExecuteClient()
databricks_client = DatabricksClient()

# Make requests
response = await vap_client.get_graph_entities(request)
```

### Integration with FastAPI

```python
from fastapi import FastAPI
from external_apis.routes import router

app = FastAPI()
app.include_router(router)
```

## 📊 Response Models

### APIResponse
```python
{
  "success": bool,
  "data": Optional[Dict[str, Any]],
  "error": Optional[str],
  "status_code": int
}
```

### DatabaseQueryResponse
```python
{
  "success": bool,
  "data": Optional[List[Dict[str, Any]]],
  "error": Optional[str],
  "row_count": Optional[int],
  "execution_time": Optional[float]
}
```

## 🔒 Security

- **Database Credentials**: Stored as AWS Secrets Manager secrets
- **API Keys**: Configured via environment variables
- **Connection Pooling**: Efficient database connection management
- **Timeout Handling**: Configurable request timeouts

## 🚨 Error Handling

The package includes comprehensive error handling:

- **HTTP Errors**: Proper status code handling
- **Timeouts**: Configurable retry logic
- **Database Errors**: Connection and query error handling
- **Validation Errors**: Pydantic model validation

## 📈 Performance

- **Async Operations**: All HTTP requests are async
- **Connection Pooling**: Database connections are pooled
- **Retry Logic**: Automatic retries for failed requests
- **Timeout Management**: Configurable timeouts for all operations

## 🧪 Testing

To test the endpoints:

```bash
# Test CCP VAP
curl "http://localhost:8000/external/getGraphEntity?branch_name=master&ccp_entity_name=abc&project_name=custom_ams_cubes"

# Test CCP Execute
curl "http://localhost:8000/external/getExecutionDetails/10449294"

# Test Databricks
curl "http://localhost:8000/external/getClientNCSDetails"

# Test Database
curl -X POST "http://localhost:8000/external/executeDBQuery" \
     -H "Content-Type: application/json" \
     -d '{"environment": "qa", "query": "SELECT 1"}'
```

## 🔄 Dependencies

Required packages:
- `fastapi`
- `httpx`
- `psycopg2-binary`
- `pydantic`

Add to requirements.txt:
```
httpx
psycopg2-binary
``` 