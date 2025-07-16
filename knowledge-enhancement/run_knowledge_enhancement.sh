#!/bin/bash

# Think AI - Legal Knowledge Enhancement Runner
# This script runs the complete knowledge enhancement pipeline

set -e

echo "🧠 Think AI - Legal Knowledge Enhancement System"
echo "=================================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if we're in the right directory
if [ ! -f "legal_knowledge_harvester.py" ]; then
    echo -e "${RED}❌ Error: Please run this script from the knowledge-enhancement directory${NC}"
    exit 1
fi

# Install dependencies
echo -e "${BLUE}📦 Installing dependencies...${NC}"
python3 -m pip install -r requirements.txt

# Create output directories
echo -e "${BLUE}📁 Creating output directories...${NC}"
mkdir -p knowledge_harvest
mkdir -p integrated_knowledge

# Stage 1: Harvest knowledge from legal sources
echo -e "${GREEN}🌐 Stage 1: Harvesting knowledge from legal sources...${NC}"
echo "Sources: Wikipedia, Project Gutenberg, arXiv, Government Documents"
echo ""

python3 legal_knowledge_harvester.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Knowledge harvesting completed successfully!${NC}"
else
    echo -e "${RED}❌ Knowledge harvesting failed!${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}📊 Harvest Summary:${NC}"
if [ -f "knowledge_harvest/harvest_summary.json" ]; then
    python3 -c "
import json
with open('knowledge_harvest/harvest_summary.json', 'r') as f:
    summary = json.load(f)
    print(f\"Total items: {summary['total_items']}\")
    print(f\"Sources: {', '.join(summary['sources_used'])}\")
    for source, count in summary['by_source'].items():
        print(f\"  {source}: {count} items\")
"
fi

echo ""

# Stage 2: Integrate knowledge into Think AI format
echo -e "${GREEN}🔄 Stage 2: Integrating knowledge into Think AI format...${NC}"
echo "Processing items, building indexes, optimizing for O(1) performance..."
echo ""

python3 knowledge_integrator.py

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Knowledge integration completed successfully!${NC}"
else
    echo -e "${RED}❌ Knowledge integration failed!${NC}"
    exit 1
fi

echo ""
echo -e "${BLUE}📊 Integration Summary:${NC}"
if [ -f "integrated_knowledge/integration_report.json" ]; then
    python3 -c "
import json
with open('integrated_knowledge/integration_report.json', 'r') as f:
    report = json.load(f)
    summary = report['integration_summary']
    print(f\"Processed items: {summary['total_items']}\")
    print(f\"Categories: {summary['categories']}\")
    print(f\"Sources: {summary['sources']}\")
    print(f\"Average confidence: {summary['average_confidence']:.3f}\")
    print(f\"Integration date: {summary['integration_date']}\")
"
fi

echo ""

# Stage 3: Deploy to Think AI system
echo -e "${GREEN}🚀 Stage 3: Deploying to Think AI system...${NC}"

# Copy knowledge files to Think AI knowledge directory
THINK_AI_KNOWLEDGE_DIR="../knowledge_storage"
if [ -d "$THINK_AI_KNOWLEDGE_DIR" ]; then
    echo "Copying knowledge files to Think AI knowledge storage..."
    
    # Create backup of existing knowledge
    if [ -d "$THINK_AI_KNOWLEDGE_DIR/enhanced_knowledge" ]; then
        echo "Creating backup of existing knowledge..."
        mv "$THINK_AI_KNOWLEDGE_DIR/enhanced_knowledge" "$THINK_AI_KNOWLEDGE_DIR/enhanced_knowledge_backup_$(date +%Y%m%d_%H%M%S)"
    fi
    
    # Copy new knowledge
    cp -r integrated_knowledge "$THINK_AI_KNOWLEDGE_DIR/enhanced_knowledge"
    cp -r knowledge_harvest "$THINK_AI_KNOWLEDGE_DIR/raw_harvest"
    
    echo -e "${GREEN}✅ Knowledge deployed to Think AI system!${NC}"
else
    echo -e "${YELLOW}⚠️  Think AI knowledge directory not found. Creating local copy...${NC}"
    mkdir -p ../knowledge_storage
    cp -r integrated_knowledge ../knowledge_storage/enhanced_knowledge
    cp -r knowledge_harvest ../knowledge_storage/raw_harvest
fi

echo ""

# Generate final report
echo -e "${BLUE}📋 Final Knowledge Enhancement Report${NC}"
echo "=========================================="

# File sizes
echo -e "${BLUE}📁 Output Files:${NC}"
if [ -d "knowledge_harvest" ]; then
    harvest_size=$(du -sh knowledge_harvest | cut -f1)
    echo "  Raw harvest: $harvest_size"
fi

if [ -d "integrated_knowledge" ]; then
    integrated_size=$(du -sh integrated_knowledge | cut -f1)
    echo "  Integrated knowledge: $integrated_size"
fi

# Count files
echo ""
echo -e "${BLUE}📄 File Breakdown:${NC}"
echo "  Harvest files: $(find knowledge_harvest -name "*.json" | wc -l) JSON files"
echo "  Integration files: $(find integrated_knowledge -name "*.json" | wc -l) JSON files"

echo ""

# Integration test
echo -e "${GREEN}🧪 Testing knowledge integration...${NC}"
python3 -c "
import json
import os

try:
    # Test knowledge database
    with open('integrated_knowledge/knowledge_database.json', 'r') as f:
        db = json.load(f)
        print(f'✅ Knowledge database: {len(db[\"items\"])} items loaded')
    
    # Test indexes
    with open('integrated_knowledge/knowledge_indexes.json', 'r') as f:
        indexes = json.load(f)
        print(f'✅ Keyword index: {len(indexes[\"keyword_index\"])} keywords indexed')
        print(f'✅ Knowledge graph: {len(indexes[\"knowledge_graph\"])} categories connected')
    
    # Test quick lookup
    with open('integrated_knowledge/quick_lookup.json', 'r') as f:
        lookup = json.load(f)
        print(f'✅ Quick lookup: {len(lookup[\"by_confidence\"])} items by confidence')
    
    print('')
    print('🎯 All knowledge structures validated successfully!')
    
except Exception as e:
    print(f'❌ Validation failed: {e}')
    exit(1)
"

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}🎉 KNOWLEDGE ENHANCEMENT COMPLETED SUCCESSFULLY!${NC}"
    echo ""
    echo -e "${BLUE}📊 Summary:${NC}"
    echo "  ✅ Legal knowledge harvested from legitimate sources"
    echo "  ✅ Knowledge processed and integrated into Think AI format"
    echo "  ✅ O(1) performance indexes created"
    echo "  ✅ Knowledge graphs and relationships built"
    echo "  ✅ All structures validated and deployed"
    echo ""
    echo -e "${YELLOW}💡 Think AI now has enhanced knowledge from:${NC}"
    echo "  📚 Wikipedia articles"
    echo "  📖 Public domain books (Project Gutenberg)"
    echo "  🎓 Academic papers (arXiv)"
    echo "  🏛️  Government documents"
    echo ""
    echo -e "${GREEN}🧠 Think AI's intelligence has been significantly enhanced!${NC}"
else
    echo -e "${RED}❌ Knowledge enhancement pipeline failed during validation!${NC}"
    exit 1
fi