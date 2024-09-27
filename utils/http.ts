import axios from "axios";
import token from "./token";
import { G_API_URL, G_APP_PLATFORM_BY, G_APP_VERSION_CODE } from "../platform";

// Base URL for the API
const BASE_URL = G_API_URL;

// Function to build the authorization header
export function buildAuthorization() {
  const tokenVal = token.get();
  return tokenVal ? `Bearer ${tokenVal}` : null;
}

// Function to build request headers
export const getRequestHeaders = () => {
  const headers = {
    Accept: "application/json",
    "Content-Type": "application/json; charset=utf-8",
    // Custom headers (uncomment as needed)
    Customversioncode: G_APP_VERSION_CODE,
    Customplatformby: G_APP_PLATFORM_BY,
  };

  const authHeader = buildAuthorization();
  if (authHeader) {
    headers.Authorization = authHeader;
  }

  return headers;
};

const apiClient = axios.create({
  baseURL: BASE_URL,
});

// Request Interceptor
apiClient.interceptors.request.use((request) => {
  request.headers = {
    ...request.headers,
    ...getRequestHeaders(),
  };
  console.log("Request:", request); // Debugging: Log request
  return request;
});

// Response Interceptor
apiClient.interceptors.response.use(
  (response) => {
    console.log("Response:", response); // Debugging: Log response
    return response.data;
  },
  (error) => {
    if (error.response) {
      console.error("Response error:", error.response); // Log detailed error response
      console.error("Error Message:", error.response.data.msg); // Log specific error message
      if (error.response.status === 401) {
        token.remove();
        window.location.href = "/login";
      }
      return Promise.reject(error.response.data);
    } else {
      console.error("Request error:", error.message); // Log request error message
      return Promise.reject(error);
    }
  }
);

const _get = (url, config = {}) => apiClient.get(url, config);
const _delete = (url, config = {}) => apiClient.delete(url, config);
const _put = (url, data = {}, config = {}) => apiClient.put(url, data, config);
const _post = (url, data = {}, config = {}) => apiClient.post(url, data, config);

export { _get, _delete, _put, _post };
