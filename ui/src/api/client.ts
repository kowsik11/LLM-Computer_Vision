import axios from "axios";

export const apiClient = axios.create({
  baseURL: "/v1"
});

export interface Job {
  id: string;
  goal: string;
  site_policy: string[];
  created_at: string;
  status: string;
  latest_run_id?: string;
}

export interface Run {
  id: string;
  job_id: string;
  started_at: string;
  finished_at?: string;
  status: string;
  metrics: Record<string, unknown>;
}

export const fetchJobs = async (): Promise<Job[]> => {
  const { data } = await apiClient.get<Job[]>("/jobs");
  return data;
};

export const createJob = async (payload: { goal: string; site_policy: string[] }) => {
  const { data } = await apiClient.post<Job>("/jobs", payload);
  return data;
};

export const fetchRuns = async (): Promise<Run[]> => {
  const { data } = await apiClient.get<Run[]>("/runs");
  return data;
};

