{{/*
Expand the name of the chart.
*/}}
{{- define "chatbot-frontend.name" -}}
{{- default .Chart.Name .Values.nameOverride -}}
{{- end -}}

{{/*
Create a default fully qualified app name.
We truncate this at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains .chart.name it is used as a full name.
*/}}
{{- define "chatbot-frontend.fullname" -}}
{{- if .Values.fullnameOverride -}}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- $name := default .Chart.Name .Values.nameOverride -}}
{{- if contains $name .Release.Name -}}
{{- .Release.Name | trunc 63 | trimSuffix "-" -}}
{{- else -}}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" -}}
{{- end -}}
{{- end -}}
{{- end -}}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "chatbot-frontend.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" -}}
{{- end -}}

{{/*
Common labels
*/}}
{{- define "chatbot-frontend.labels" -}}
helm.sh/chart: {{ include "chatbot-frontend.chart" . }}
{{ include "chatbot-frontend.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end -}}

{{/*
Selector labels
*/}}
{{- define "chatbot-frontend.selectorLabels" -}}
app.kubernetes.io/name: {{ include "chatbot-frontend.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end -}}

{{/*
Create the name of the service account to use
*/}}
{{- define "chatbot-frontend.serviceAccountName" -}}
{{- if .Values.serviceAccount.create -}}
    {{- default (include "chatbot-frontend.fullname" .) .Values.serviceAccount.name -}}
{{- else -}}
    {{- default "default" .Values.serviceAccount.name -}}
{{- end -}}
{{- end -}}