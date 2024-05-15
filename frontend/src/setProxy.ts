import { createProxyMiddleware } from 'http-proxy-middleware';

const API_URL = process.env.REACT_APP_API_URL;
export default function(app: any) {
    app.use(
        '/api',
        createProxyMiddleware({
            target: API_URL,
            changeOrigin: true,
        })
    );
}
