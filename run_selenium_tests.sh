#!/bin/bash
# Selenium Test Runner for LocalFinds
# This script starts the app and runs Selenium tests

set -e

echo "🚀 Starting LocalFinds Selenium Test Suite"
echo "=========================================="

# Check if app is already running
if curl -s http://127.0.0.1:5000 > /dev/null 2>&1; then
    echo "✅ App appears to be running on http://127.0.0.1:5000"
    APP_RUNNING=true
else
    echo "📱 Starting Flask app..."
    make run &
    APP_PID=$!
    echo "✅ App started with PID: $APP_PID"

    # Wait for app to be ready
    echo "⏳ Waiting for app to be ready..."
    for i in {1..30}; do
        if curl -s http://127.0.0.1:5000 > /dev/null 2>&1; then
            echo "✅ App is ready!"
            break
        fi
        sleep 1
    done

    if ! curl -s http://127.0.0.1:5000 > /dev/null 2>&1; then
        echo "❌ App failed to start"
        exit 1
    fi
fi

echo ""
echo "🧪 Running Selenium tests..."
echo "=============================="

# Run Selenium tests
PYTHONPATH=. venv/bin/pytest tests/test_selenium.py -v --tb=short

TEST_EXIT_CODE=$?

echo ""
echo "🧹 Cleaning up..."

# Stop app if we started it
if [ "$APP_RUNNING" != true ] && [ ! -z "$APP_PID" ]; then
    echo "Stopping app (PID: $APP_PID)..."
    kill $APP_PID 2>/dev/null || true
    wait $APP_PID 2>/dev/null || true
    echo "✅ App stopped"
fi

echo ""
if [ $TEST_EXIT_CODE -eq 0 ]; then
    echo "🎉 All Selenium tests passed!"
else
    echo "❌ Some Selenium tests failed"
fi

exit $TEST_EXIT_CODE