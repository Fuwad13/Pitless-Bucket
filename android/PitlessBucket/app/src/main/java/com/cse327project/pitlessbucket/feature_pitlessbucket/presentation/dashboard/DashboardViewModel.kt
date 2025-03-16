package com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch

data class DashboardState(
    val files: List<FileInfo> = emptyList(),
    val isLoading: Boolean = false,
    val error: String? = null
)

class DashboardViewModel(private val apiService: ApiService) : ViewModel() {
    private val _state = MutableStateFlow(DashboardState())
    val state: StateFlow<DashboardState> = _state

    fun setIdToken(idToken: String) {
        fetchFiles(idToken)
    }

    private fun fetchFiles(idToken: String) {
        viewModelScope.launch {
            _state.value = _state.value.copy(isLoading = true)
            try {
                val files = apiService.getFiles("Bearer $idToken")
                _state.value = _state.value.copy(files = files, isLoading = false)
                println(_state.value)
            } catch (e: Exception) {
                _state.value = _state.value.copy(error = e.message, isLoading = false)
            }
        }
    }

    fun downloadFile(idToken: String, fileId: String){
        viewModelScope.launch {

        }
    }
}