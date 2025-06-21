
const results = {imports: {}, functionality: {}};

// Test imports
const libraries = [
    ["think-ai-js", "think-ai-js"],
    ["@think-ai/cli", "@think-ai/cli"],
    ["o1-js", "o1-js"]
];

for (const [importName, libName] of libraries) {
    try {
        require(importName);
        results.imports[libName] = {success: true};
    } catch (e) {
        results.imports[libName] = {success: false, error: e.message};
    }
}

// Test Think AI client
try {
    const {ThinkAI} = require("think-ai-js");
    const client = new ThinkAI({apiUrl: "http://localhost:8000"});
    results.functionality.client_creation = {success: true};
} catch (e) {
    results.functionality.client_creation = {success: false, error: e.message};
}

// Test O1 vector search
try {
    const {O1VectorSearch} = require("o1-js");
    const search = new O1VectorSearch(128);
    results.functionality.vector_search_js = {success: true};
} catch (e) {
    results.functionality.vector_search_js = {success: false, error: e.message};
}

console.log(JSON.stringify(results));
