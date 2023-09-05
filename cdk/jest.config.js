module.exports = {
  testEnvironment: 'node',
  roots: ['<rootDir>/test', '<rootDir>/lib'],
  testMatch: ['**/*.test.ts'],
  transform: {
    '^.+\\.tsx?$': 'ts-jest'
  },
  testPathIgnorePatterns: [
    '/node_modules/'
  ],
  collectCoverage: true,
  coverageDirectory: 'coverage',
  collectCoverageFrom: ['lib/**/*.{ts,tsx}']
};
