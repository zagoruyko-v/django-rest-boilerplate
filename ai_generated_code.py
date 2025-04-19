Предположим, мы имеем дело с реальным преградой в коде, представленной пулом запросов (PR). Для анализа и решения этой проблемы мы воспользуемся следующими шагами:

**Анализ PR:**

PR находит место для cảiрения использования глобальных переменных вместо передачи их в методы. Поскольку это не простая задача, но проблема важности, ее нужно решить.

**Пул запросов:**
`fix/cleanup-global-variables`

* **Description:** "Cleanup global variables usage"
* **Body:** "Remove unnecessary global variable usages in the codebase"
* **Changes:**
	+ Remove unused global variable `globalVariable1`
	+ Replace multiple instances of `globalVariable2` with function parameters
	+ Rename some global variables to follow camelCase convention

**Репозиторий:**

На данном этапе мы не знаем подробности реального кода, поэтому будем ориентироваться на общие принципы и рекомендации.

**Кодbase:**
```typescript
// global-variable1.ts
const globalVariable1 = 'some_value';

function doSomething() {
  console.log(globalVariable1); // unused global variable usage
}

export default function somethingElse() {
  return 'some_other_value';
}
```

```javascript
// another-file.js
const globalVariable2 = 'another_global_variable';

function doSomeOtherThing() {
  console.log(globalVariable2);
}
```

```typescript
// final-file.ts
let globalVariable3 = 'third_global_variable';

function doFinalThing() {
  console.log(globalVariable3);
}

export function finalExportFunction() {
  return 'some_export_value';
}
```
**Проблемы и подход к решению:**

* В первом сценарии (globalVariable1) нам нужно убедиться, что все instances globalVariable1 будут заменены на соответствующие функциональные parameters.
* Во втором сценарии (globalVariable2) нам нужно определить, можно ли вынести это в отдельную переменную или же использовать someOtherFunction для этой цели.
* В третьем сценарии (globalVariable3), мы должны убедиться, что all instances будут заменены на соответствующие функциональные параметры и приведен в соответствие camelCase.

**Фикстуры:**

### 1. Remove unused global variable usage

```typescript
// src/lib/global-variables.js
export function isGlobalVariableUsed(name: string): boolean {
  return !isUndefined(process.env[name]);
}

export default function cleanupUnusedGlobals() {
  const usedVariables = [];
  for (const key in process.env) {
    if (process.env[key] !== undefined && !isGlobalVariableUsed(key)) {
      console.warn(`Removing unused global variable: ${key}`);
    }
  }

  return usedVariables;
}
```
### 2. Replace multiple instances of `globalVariable2` with function parameters

```typescript
// src/lib/other-functions.js
export default function doSomeOtherThing(variableName: string) {
  console.log(variableName);
}

export function someOtherFunction() {
  doSomeOtherThing('another_global_variable');
}
```

### 3. Rename global variables to follow camelCase convention

```typescript
// src/lib/global-variables.ts
export const SOME_CAMEL_CASE_VARIABLE = 'some_camel_case_value';

export function renameGlobalVariables() {
  for (const key in process.env) {
    if (isUpperCamel(process.env[key])) {
      process.env[key] = convertToCamelCase(key);
      console.log(`Renamed global variable: ${key} to ${convertToCamelCase(key)}`);
    }
  }
}

function isUpperCamel(str: string): boolean {
  const firstChar = str.charAt(0).toUpperCase();
  return !isLowercase(firstChar);
}

function convertToCamelCase(str: string): string {
  const words = str.split('_');
  return words.reduce((str, word) => `${word.charAt(0).toUpperCase()}${word.slice(1)}`, '');
}
```
### 4. Replace globalVariable3 with function parameters

```typescript
// src/lib/third-file.ts
let thirdGlobalVariable = 'third_global_variable';

export default function doFinalThing() {
  console.log(thirdGlobalVariable);
}

export function finalExportFunction() {
  return 'some_final_export_value';
}
```

```typescript
// src/lib/final-export-function.ts
function finalExportFunction(variableName: string) {
  console.log(variableName);
}

export default function someOtherFinalExportFunction() {
  finalExportFunction('third_global_variable');
}
```
**Тесты:**

### Unit tests for `cleanupUnusedGlobals`

```typescript
// tests/cleanup-unused-globals.test.ts
import { cleanupUnusedGlobals } from './lib/global-variables';

jest.mock('../environment')

beforeEach(() => {
  process.env = {};
})

afterEach(() => {
  delete require.cache[require.resolve('../environment')]
  process.env = {};
})

it('should log unused global variables', () => {
  process.env.ANONYMOUS_GLOBAL_VARIABLE = 'some_global_value';
  cleanupUnusedGlobals();

  expect(console.error).toHaveBeenCalledTimes(1);
});

it('should not return used variables', async () => {
  const mockUsedVariables = [];
  await cleanupUnusedGlobals();
  expect(mockUsedVariables).toBe([]);
});
```
### Unit tests for `renameGlobalVariables`

```typescript
// tests/rename-global-variables.test.ts
import { renameGlobalVariables } from './lib/global-variables';

beforeEach(() => {
  process.env = {};
})

afterEach(() => {
  delete require.cache[require.resolve('./lib/global-variables')]
  process.env = {};
})

it('should rename global variables', async () => {
  process.env.GLOBAL_VARIABLE_1 = 'some_global_variable_1';
  await renameGlobalVariables();

  expect(process.env.SOME_CAMEL_CASE_VARIABLE).toBe('some_global_variable_1');
});

it('should log renaming of variables without errors', async () => {
  renameGlobalVariables();
  expect(console.log).toHaveBeenCalledTimes(1);
});
```
### Integration tests for `cleanupUnusedGlobals` and `renameGlobalVariables`

```typescript
// tests/integration/global-variables.test.ts
import { cleanupUnusedGlobals, renameGlobalVariables } from './lib/global-variables';

beforeEach(() => {
  process.env = {};
})

afterEach(() => {
  delete require.cache[require.resolve('./lib/global-variables')]
  process.env = {};
})

it('should fix global variables usage', async () => {
  const mockUsedVariables = [];
  await cleanupUnusedGlobals();
  expect(mockUsedVariables).toBe([]);
});

it('should fix renaming of global variables to camelCase convention', async () => {
  renameGlobalVariables();
  expect(process.env.SOME_CAMEL_CASE_VARIABLE).toBe('some_global_variable_1');
});
```
### Integration tests for `renameGlobalVariables`

```typescript
// tests/integration/renaming-global-variables.test.ts
import { renameGlobalVariables } from './lib/global-variables';

beforeEach(() => {
  process.env = {};
})

afterEach(() => {
  delete require.cache[require.resolve('./lib/global-variables')]
  process.env = {};
})

it('should rename global variables', async () => {
  renameGlobalVariables();
  expect(console.log).toHaveBeenCalledTimes(1);
});
```
Мы создали фикстуры и тесты для решения этой проблемы, в которой исполняем различные сценарии и проверяем результат.

Примечание: В этом примере мы используем TypeScript, но принципы также применимы к JavaScript.