package com.cse327project.pitlessbucket.feature_pitlessbucket.domain.model

data class FileDashboardUiState(
    val files: List<FileInfo> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)
