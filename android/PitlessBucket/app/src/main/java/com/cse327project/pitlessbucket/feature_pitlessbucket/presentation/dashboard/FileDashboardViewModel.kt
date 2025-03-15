package com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.cse327project.pitlessbucket.feature_pitlessbucket.data.repository.FileRepository
import com.cse327project.pitlessbucket.feature_pitlessbucket.domain.model.FileDashboardUiState
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

class FileDashboardViewModel(private val fileRepository: FileRepository) : ViewModel() {

    private val _uiState = MutableStateFlow(FileDashboardUiState(isLoading = true))
    val uiState: StateFlow<FileDashboardUiState> = _uiState.asStateFlow()

    init {
        fetchFiles()
    }

    fun fetchFiles() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }

            fileRepository.getFiles()
                .onSuccess { files ->
                    _uiState.update {
                        it.copy(files = files, isLoading = false, error = null)
                    }
                }
                .onFailure { exception ->
                    _uiState.update {
                        it.copy(isLoading = false, error = exception.message)
                    }
                }
        }
    }
}