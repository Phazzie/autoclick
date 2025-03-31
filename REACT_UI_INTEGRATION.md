# AUTOCLICK React UI Integration

This document provides instructions for integrating the React UI with the Python backend for the AUTOCLICK application.

## Overview

The integration uses a REST API approach:

1. The React UI runs as a web application (Next.js)
2. The Python backend exposes a REST API using Flask
3. The React UI communicates with the Python backend via API calls

## Setup Instructions

### 1. Install Dependencies

First, install the required Python dependencies:

```bash
python setup_api.py
```

This will install Flask and Flask-CORS, which are needed for the API server.

### 2. Set Up the React UI

Navigate to the React UI directory and install dependencies:

```bash
cd "UI FROM VERCEL"
npm install
# or
pnpm install
```

### 3. Start the API Server

In one terminal, start the Python API server:

```bash
python api_server.py
```

The API server will run on http://localhost:5000.

### 4. Start the React UI

In another terminal, start the React UI development server:

```bash
cd "UI FROM VERCEL"
npm run dev
# or
pnpm dev
```

The React UI will be available at http://localhost:3000.

## API Endpoints

The API server provides the following endpoints:

- `GET /api/workflows` - Get all workflows
- `GET /api/workflows/{id}` - Get a specific workflow
- `POST /api/workflows` - Create a new workflow
- `PUT /api/workflows/{id}` - Update an existing workflow
- `DELETE /api/workflows/{id}` - Delete a workflow
- `POST /api/workflows/{id}/execute` - Execute a workflow
- `GET /api/workflow-types` - Get available workflow step types

## Architecture

### Components

1. **React UI**: Modern, responsive user interface built with Next.js, React, and Tailwind CSS
2. **API Server**: Flask-based REST API that exposes the Python backend functionality
3. **Workflow Adapter**: Converts between frontend and backend workflow representations
4. **Backend Services**: Existing AUTOCLICK services for workflow management and execution

### Data Flow

1. User interacts with the React UI
2. UI makes API calls to the Python backend
3. Backend processes the requests and returns responses
4. UI updates based on the responses

## Troubleshooting

### CORS Issues

If you encounter CORS issues, make sure the Flask-CORS package is installed and properly configured in the API server.

### API Connection Issues

If the UI cannot connect to the API:
- Ensure the API server is running on http://localhost:5000
- Check that there are no firewall or network issues blocking the connection
- Verify that the API endpoints are correctly implemented

### Workflow Execution Issues

If workflow execution fails:
- Check the Python console for error messages
- Verify that the workflow steps are properly formatted
- Ensure that the execution engine is properly initialized

## Next Steps

After successfully integrating the React UI with the Python backend, consider:

1. Implementing authentication for API security
2. Adding more advanced workflow features
3. Improving error handling and user feedback
4. Creating a production build for deployment
