package com.dokmatiq.docgen.client;

import com.dokmatiq.docgen.exception.DocGenException;
import com.dokmatiq.docgen.internal.Transport;
import com.dokmatiq.docgen.model.ComposeRequest;
import com.dokmatiq.docgen.model.DocumentRequest;
import com.dokmatiq.docgen.model.JobInfo;

import java.util.List;

/** Client for document generation endpoints. */
public class DocumentsClient {
    private final Transport transport;

    public DocumentsClient(Transport transport) {
        this.transport = transport;
    }

    /** Generate a document synchronously. */
    public byte[] generate(DocumentRequest request) {
        return transport.requestBytes("POST", "/api/documents/generate", request);
    }

    /** Compose a multi-part document. */
    public byte[] compose(ComposeRequest request) {
        return transport.requestBytes("POST", "/api/documents/compose", request);
    }

    /** Submit an async generation job. */
    public JobInfo generateAsync(DocumentRequest request) {
        return transport.requestJson("POST", "/api/documents/generate-async", request, JobInfo.class);
    }

    /** Get status of an async job. */
    public JobInfo getJob(String jobId) {
        return transport.requestJson("GET", "/api/documents/jobs/" + jobId, null, JobInfo.class);
    }

    /** Download the result of a completed async job. */
    public byte[] downloadJob(String jobId) {
        return transport.requestBytes("GET", "/api/documents/jobs/" + jobId + "/download", null);
    }

    /** List recent async jobs. */
    public List<JobInfo> listJobs() {
        return transport.requestList("GET", "/api/documents/jobs", JobInfo.class);
    }

    /**
     * Poll an async job until completion.
     *
     * @param jobId        Job ID to poll.
     * @param pollInterval Interval in ms between polls.
     * @param timeout      Maximum wait time in ms.
     * @return The generated document bytes.
     */
    public byte[] waitForJob(String jobId, long pollInterval, long timeout) {
        long deadline = System.currentTimeMillis() + timeout;

        while (System.currentTimeMillis() < deadline) {
            var job = getJob(jobId);

            if ("COMPLETED".equals(job.status().getValue())) {
                return downloadJob(jobId);
            }
            if ("FAILED".equals(job.status().getValue())) {
                throw new DocGenException("Job " + jobId + " failed: " +
                        (job.errorMessage() != null ? job.errorMessage() : "unknown error"));
            }

            long remaining = deadline - System.currentTimeMillis();
            if (remaining <= 0) break;

            try {
                Thread.sleep(Math.min(pollInterval, remaining));
            } catch (InterruptedException e) {
                Thread.currentThread().interrupt();
                throw new DocGenException("Polling interrupted", e);
            }
        }

        throw new DocGenException("Job " + jobId + " did not complete within " + timeout + "ms");
    }

    /** Poll with default settings (2s interval, 120s timeout). */
    public byte[] waitForJob(String jobId) {
        return waitForJob(jobId, 2000, 120_000);
    }
}
