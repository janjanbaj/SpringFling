export { matchers } from './client-matchers.js';

			export const nodes = [() => import('./nodes/0'),
	() => import('./nodes/1'),
	() => import('./nodes/2'),
	() => import('./nodes/3'),
	() => import('./nodes/4'),
	() => import('./nodes/5'),
	() => import('./nodes/6'),
	() => import('./nodes/7'),
	() => import('./nodes/8')];

			export const server_loads = [0];

			export const dictionary = {
	"": [3],
	"(authenticated)/dashboard": [4,[2]],
	"(authenticated)/settings": [5,[2]],
	"login": [~6],
	"logout": [~7],
	"signup": [~8]
};

			export const hooks = {
				handleError: (({ error }) => { console.error(error); return { message: 'Internal Error' }; }),
			};