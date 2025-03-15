package com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.file_upload

import android.net.Uri
import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.cse327project.pitlessbucket.feature_pitlessbucket.presentation.dashboard.ApiService
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.launch
import okhttp3.MultipartBody

class FileUploadViewModel(private val apiService: ApiService) : ViewModel() {
    private val _state = MutableStateFlow(FileUploadState())
    val state: StateFlow<FileUploadState> = _state

    fun selectFile(uri: Uri) {
        _state.value = _state.value.copy(selectedFileUri = uri)
    }


    fun uploadFile(idToken: String, filePart: MultipartBody.Part) {
        viewModelScope.launch {
            _state.value = _state.value.copy(isUploading = true, error = null)
            try {
                val response = apiService.uploadFile("Bearer $idToken", filePart)
                if (response.isSuccessful) {
                    _state.value = _state.value.copy(
                        uploadResponse = response.body(),
                        isUploading = false
                    )
                } else {
                    _state.value = _state.value.copy(
                        error = "Upload failed: ${response.code()}",
                        isUploading = false
                    )
                }
            } catch (e: Exception) {
                _state.value = _state.value.copy(
                    error = e.message,
                    isUploading = false
                )
            }
        }
    }
}
