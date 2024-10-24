// store.js
import { writable } from 'svelte/store';

export const currentVariableIndex = writable(0);
export const variables = ['ft_employment', 'ft_pay', 'another_variable'];