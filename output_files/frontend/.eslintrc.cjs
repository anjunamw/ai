# frontend/.eslintrc.cjs
module.exports = {
  root: true,
  env: {
    browser: true,
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    '@vue/eslint-config-typescript',
  ],
  parserOptions: {
      ecmaVersion: 2021,
    sourceType: 'module',
      parser: '@typescript-eslint/parser',
  },
  plugins: ['@typescript-eslint'],
  rules: {
    // Add any custom rules here
  },
}