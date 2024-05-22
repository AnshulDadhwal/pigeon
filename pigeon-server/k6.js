import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  stages: [
    { target: 1000, duration: '1m' },
    { target: 5000, duration: '10m' },
  ],
};

const BASE_URL = 'http://${aws_lb.server.dns_name}/api/v1';

export default function () {
  // Test GET request to the health endpoint
  const healthRes = http.get(`${BASE_URL}/health`);
  check(healthRes, {
    'health status was 200': (r) => r.status === 200,
    'health response contains "status": "ok"': (r) => JSON.parse(r.body).status === 'ok',
  });

  // Test GET request to retrieve unreceived messages for a user
  const pigeonId = '550e8400-e29b-41d4-a716-446655440000';
  const getMessageRes = http.get(`${BASE_URL}/messages/${pigeonId}`);
  check(getMessageRes, {
    'get messages status was 200': (r) => r.status === 200,
    'get messages response is JSON': (r) => r.headers['Content-Type'] === 'application/json',
  });

  // Test POST request to store a new message
  const messagePayload = JSON.stringify({
    meta: {
      from: '123e4567-e89b-12d3-a456-426614174000',
      to: pigeonId,
      datetime: new Date().toISOString(),
    },
    message: 'Hello, Pigeon!',
  });
  const headers = { 'Content-Type': 'application/json' };
  const postMessageRes = http.post(`${BASE_URL}/messages/${pigeonId}`, messagePayload, { headers });
  check(postMessageRes, {
    'post message status was 201': (r) => r.status === 201,
    'post message response is JSON': (r) => r.headers['Content-Type'] === 'application/json',
  });

  sleep(1);
}
