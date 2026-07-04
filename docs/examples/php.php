<?php
/**
 * SdashAPI — PHP Example
 * ======================
 * No dependencies required — uses built-in cURL.
 * PHP 7.4+
 */

define('SDASH_TOKEN', 'sdash_your_token_here'); // Replace with your AccessToken
define('SDASH_BASE',  'https://sdashapi.com/api/v1');

/**
 * Make a GET request to the SdashAPI
 */
function sdash_get(string $endpoint, array $params = []): array
{
    $url = SDASH_BASE . $endpoint;
    if ($params) {
        $url .= '?' . http_build_query($params);
    }

    $ch = curl_init($url);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_HTTPHEADER     => ['AccessToken: ' . SDASH_TOKEN],
        CURLOPT_TIMEOUT        => 10,
    ]);

    $body   = curl_exec($ch);
    $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($body === false || $status !== 200) {
        throw new RuntimeException("SdashAPI error: HTTP $status");
    }

    return json_decode($body, true);
}

/**
 * Make a POST request to the SdashAPI
 */
function sdash_post(string $endpoint, array $payload): array
{
    $ch = curl_init(SDASH_BASE . $endpoint);
    curl_setopt_array($ch, [
        CURLOPT_RETURNTRANSFER => true,
        CURLOPT_POST           => true,
        CURLOPT_POSTFIELDS     => json_encode($payload),
        CURLOPT_HTTPHEADER     => [
            'AccessToken: ' . SDASH_TOKEN,
            'Content-Type: application/json',
        ],
        CURLOPT_TIMEOUT => 10,
    ]);

    $body   = curl_exec($ch);
    $status = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    return json_decode($body, true);
}

// ----------------------------------------------------------
// 1. Get a single random question
// ----------------------------------------------------------
echo "=== Random Question ===\n";
$res = sdash_get('/q');
$q   = $res['data'];
echo $q['question'] . "\n";
foreach ($q['option'] as $key => $val) {
    $marker = ($key === $q['answer']) ? '✅' : '  ';
    echo "  $marker " . strtoupper($key) . ") $val\n";
}
if ($q['solution']) echo "  💡 " . $q['solution'] . "\n";

// ----------------------------------------------------------
// 2. Filtered questions
// ----------------------------------------------------------
echo "\n=== UTME Chemistry 2022 (3 questions) ===\n";
$res = sdash_get('/q', [
    'subject' => 'chemistry',
    'type'    => 'utme',
    'year'    => 2022,
    'limit'   => 3,
]);
foreach ($res['data'] as $i => $q) {
    echo "\nQ" . ($i + 1) . ": " . $q['question'] . "\n";
    echo "   Exam: {$q['examtype']} {$q['examyear']}\n";
}

// ----------------------------------------------------------
// 3. List subjects
// ----------------------------------------------------------
echo "\n=== Subjects ===\n";
$res = sdash_get('/subjects');
foreach ($res['data'] as $s) {
    printf("  %-30s slug: %s\n", $s['name'], $s['slug']);
}

// ----------------------------------------------------------
// 4. List exam types
// ----------------------------------------------------------
echo "\n=== Exam Types ===\n";
$res = sdash_get('/exams');
foreach ($res['data'] as $e) {
    printf("  %-20s slug: %s\n", $e['name'], $e['slug']);
}

// ----------------------------------------------------------
// 5. List available years
// ----------------------------------------------------------
echo "\n=== Available Years ===\n";
$res = sdash_get('/years');
echo implode(', ', $res['data']) . "\n";

// ----------------------------------------------------------
// 6. Report a question
// ----------------------------------------------------------
// $result = sdash_post('/report', [
//     'question_id' => 4821,
//     'report_type' => 'wrong_answer',
//     'message'     => 'Option B should be correct.',
// ]);
// echo $result['message'] . "\n";
